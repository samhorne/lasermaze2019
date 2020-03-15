# Laser Maze 2019

For this year's Halloween, some friends and I decided to go all out and build an immersive laser maze. This quickly became the largest project I have ever undertaken, and challenged me to learn new things. Feel free to use this code for your own laser maze.

<img src="/2019%20Laser%20Maze%20Block%20Diagram.png" width=90% alt="Block diagram">

### Links
- [Hardware Setup](https://samhorne.github.io/lasermaze)
- Other code written for this project
  - iOS App (Swift)
  - MQTT to Core MIDI (Python)
  - [MQTT Video Trigger (Processing)](https://github.com/samhorne/mqtt-video-trigger)
  - Leaderboard (Processing)

### Installation
Tested on a Raspberry Pi 2 Model B running Raspbian GNU/Linux 10 (buster).
1. Setup virtual environment.
```sh
$ pip install virtualenv
$ virtualenv laser-maze
$ source laser-maze/bin/activate
```
2. Inside that virtual environment, clone the repository.
```sh
$ cd laser-maze
$ git clone https://github.com/samhorne2/lasermaze2019.git
```
3. Install the requirements.
```sh
$ pip install -r requirements.txt
```
4. Install and start mosquitto.
```sh
$ sudo apt install mosquitto
$ sudo systemctl enable mosquitto
```
5. Edit mqtt_send.py and mqtt-recieve.py with the IP address of your new MQTT broker.
- mqtt_recieve.py -> line 25
- mqtt_send.py -> line 22
```python
client.connect("192.168.1.133", 1883, 60) #Your MQTT broker IP address here.
```
### Setup the Game
1. Run mqtt_recieve.py to begin listening for the following messages on the topic "maze".
```sh
$ python3 mqtt_recieve.py
```
| MQTT Message        |    Description |
| ------------- |-------------|
|   "arm"       | Activates all lasers and begins detecting sensors intrusions.|
| "aimblink"     | Blinks lasers whose sensors are intruded for aiming purposes.|
| "thresh" | Set thresholds for each beam (the average brightness between laser on and off).|
| "reset" | End the current game or stop aimblink.|
|"exit"| Exit the entire game.|

If you haven't setup the custom iOS app I made for this, you can easily use a tool such as [MQTTool](https://apps.apple.com/us/app/mqttool/id1085976398).

Like this project? Check out my other projects [here](https://samhorne.github.io)!
