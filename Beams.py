from gpiozero import LED as Laser
import sensors

class Beam:
    def __init__(self, laser_pin, sensor_pin, threshold):
        self.laser = Laser(laser_pin)
        self.sensor_pin = sensor_pin
        self.threshold = threshold
        self.is_blinking = False
    def get_sensor_value(self):
        return sensors.photoresistor_read(self.sensor_pin)

beams = {}
beams[0] = Beam(0, 13, 500)
beams[1] = Beam(1, 5, 500)
beams[4] = Beam(4, 17, 500)
beams[5] = Beam(5, 5, 300)
beams[6] = Beam(6, 6, 200)
#beams[7] = Beam(7, 7, 400)
beams[8] = Beam(8, 8, 200)
beams[9] = Beam(9, 9, 100)
beams[10] = Beam(10, 10, 100)
beams[11] = Beam(11, 11, 100)
beams[12] = Beam(12, 18, 300)
beams[13] = Beam(13, 13, 1)
beams[14] = Beam(14, 14, -5)
beams[15] = Beam(15, 9, 200)
beams[16] = Beam(16, 16, 200)
beams[17] = Beam(17, 17, 200)
beams[18] = Beam(18, 18, 200)
beams[19] = Beam(19, 12, 10)
beams[20] = Beam(20, 16, 10)
beams[21] = Beam(21, 11, 500)
beams[22] = Beam(22, 6, 10)
beams[23] = Beam(23, 8, 10)
beams[24] = Beam(24, 10, 200)
beams[25] = Beam(25, 19, 300)
beams[26] = Beam(26, 7, 50)
beams[27] = Beam(27, 15, 300)

class MazeDifficultyProfile:
    def __init__(self, beam_keys):
        self.beam_keys = beam_keys
    def lasers_on(self):
        for bK in self.beam_keys:
            beams[bK].laser.on()
            beams[bK].is_blinking = False
    def lasers_off(self):
        for bK in self.beam_keys:
            beams[bK].laser.off()
            beams[bK].is_blinking = False
    def get_sensor_pins(self):
        sensor_pins = []
        for bK in self.beam_keys:
            sensor_pins.append(beams[bK].sensor_pin)
            #print("Current sensor pin: " + beams[bK].sensor_pin)
        return sensor_pins
