from time import sleep, perf_counter
from Beams import Beam, MazeDifficultyProfile, beams
import sensors, random, threading, sys
from gpiozero import Button
from signal import pause
from mqtt2 import send_msg
#from mqtt import send_msg

diff_profiles = {}
diff_profiles["allMaster"] = MazeDifficultyProfile([0,1,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27])
diff_profiles["master"] = MazeDifficultyProfile([0,1,4,12,15,19,20,21,22,23,24,25,26,27])
diff_profiles["easy"] = MazeDifficultyProfile([22,23,24,25,26,27])
diff_profiles["medium"] = MazeDifficultyProfile([0,1,4,12,15,19,20,21,23,25,26,27])
current_diff_profile_key = "easy"

button = Button(7, False, bounce_time = .7) #CE1 pin (GPIO7)
game_stopped = True
continue_current_thread = True

def begin_intrusion_detection():
    send_msg("triggerVideoMain", "videoCue")
    global current_diff_profile_key
    global game_stopped
    try:
        dP = diff_profiles[current_diff_profile_key]
    except:
        dP = diff_profiles["master"]
    all_lasers_off()
    dP.lasers_on()
    sleep(.3)
    #print("Ready")
    intrusions = 0
    #while(intrusions < len(dP.beam_keys) and not game_stopped):
    while(intrusions < 3 and not game_stopped):
        for bK in dP.beam_keys:
            #print("Beam " + str(b.laser.pin)[4:] + " status: " + str(b.laser.is_lit))
            if(beams[bK].get_sensor_value() < beams[bK].threshold and beams[bK].laser.is_lit):
                beams[bK].laser.off()
                print("Beam " + str(beams[bK].laser.pin)[4:] + " intruded.")
                intrusions = intrusions + 1
                sleep(.01)
                print("gip = {}".format(gip))
            pass
    if (intrusions >= 3):
        send_msg("triggerVideoFail", "videoCue")
    all_lasers_off()
    game_stopped = True
    #mqtt.send_msg("fail")


def standby_random_chase(speed=.8):
    last_rand = -1
    while(True):
        rand = random.choice(list(beams))
        while (rand == last_rand):
            rand = random.choice(list(beams))
        beams[rand].laser.on()
        sleep(speed)
        beams[rand].laser.off()
        last_rand = rand

def aim_blink():
    global continue_current_thread
    print('aim_blink()')
    diff_profiles["master"].lasers_on()
    while(continue_current_thread):
        sleep(.05)
        for a in beams.values():
            if(a.get_sensor_value() < a.threshold and not a.is_blinking):
                print("Beam " + str(a.laser.pin)[4:] + " intruded.")
                a.laser.blink(on_time = .2, off_time = .2)
                a.is_blinking = True
            elif(a.get_sensor_value() > a.threshold and a.is_blinking):
                print("Beam " + str(a.laser.pin)[4:] + " clear.")
                a.laser.on()
                a.is_blinking = False
    all_lasers_off()

def set_thresholds():
    all_lasers_off()
    sleep(1)
    dark_levels = sensors.get_all_photoresistor_values()
    print("DARK ------")
    print(dark_levels)
    all_lasers_on()
    sleep(1)
    bright_levels = sensors.get_all_photoresistor_values()
    print("BRIGHT -----")
    print(bright_levels)
    sleep(1)
    for i in beams:
        sPin = beams[i].sensor_pin
        print("Beam: " + str(i))
        print("Sensor: " + str(sPin))
        print(" -> OLD: " + str(beams[i].threshold))
        print("    LOW: " + str(dark_levels[sPin]))
        print("    HIGH: " + str(bright_levels[sPin]))
        threshold = (dark_levels[sPin] + bright_levels[sPin])/2
        beams[i].threshold = threshold
        print("    NEW: " + str(threshold))
    all_lasers_off()
    continue_current_thread = False

def all_lasers_on():
    diff_profiles["master"].lasers_on()

def all_lasers_off():
    diff_profiles["master"].lasers_off()

def start_game():
    global game_stopped
    game_stopped = False
    game_thread = threading.Thread(target = begin_intrusion_detection, name = 'game_thread')
    game_thread.daemon = True
    game_thread.start()
    start_time = perf_counter()
    #sleep(.5)
    while(button.is_pressed and not game_stopped):
        sleep(.01)
    if game_stopped:
        pass
    else:
        send_msg("triggerVideoWin", "videoCue")
    print("Game stopped by: beam trip." if game_stopped else "Game stopped by: button." )
    stop_time = perf_counter()
    elapsed_time = stop_time - start_time
    print("Elapsed time: " + str(elapsed_time))
    send_msg(str(elapsed_time))
    game_stopped = True
    all_lasers_off()
    game_thread.join()

def accept_user_input(user_command):
    global continue_current_thread
    global game_stopped
    #user_command = input("Enter a command: ").lower()
    user_command = user_command.lower()
    if user_command == "reset":
        send_msg("triggerVideoMain", "videoCue")
        continue_current_thread = False
        if game_stopped:
            print("There is not a game in progress.")
        else:
            try:
                game_stopped = True
                main_thread.join()
                print("Disarmed")
            except NameError:
                print("Could not end the current thread.")
                pass
    elif user_command[0:3] == "arm":
        global current_diff_profile_key
        current_diff_profile_key = user_command[3:]
        continue_current_thread = False
        try:
            if main_thread.is_alive() is True:
                main_thread.join()
        except NameError:
            pass
        if not game_stopped:
            print("There is already a game in progress.")
        else:
            main_thread = threading.Thread(target = start_game, name = 'main_thread')
            main_thread.daemon = True
            print("Armed")
            main_thread.start()
    elif user_command == "exit":
        sys.exit()
    elif user_command == "aimblink":
        try:
            if main_thread.is_alive() is True:
                game_stopped = True
                main_thread.join()
                print("Disarmed")
        except NameError:
            pass
        main_thread = threading.Thread(target = aim_blink, name = 'blinkThread')
        main_thread.daemon = True
        continue_current_thread = True
        main_thread.start()
    elif user_command == "thresh":
        #reset
        continue_current_thread = False
        try:
            if main_thread.is_alive() is True:
                main_thread.join()
        except NameError:
            print("No thread found: main_thread")
            pass
        game_stopped = True
        print("Disarmed")
        #Thresholds
        print("Set thresholds")
        main_thread = threading.Thread(target = set_thresholds, name = 'set_thresholds')
        main_thread.daemon = True
        continue_current_thread = True
        main_thread.start()
