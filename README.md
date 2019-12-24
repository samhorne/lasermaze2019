# Laser Maze 2019

For this year's Halloween, some friends and I decided to go all out and build an immersive laser maze. This quickly became the largest project I have ever undertaken, and challenged me to learn new things. Feel free to use this code for your own laser maze.

### Links
- Overall Project Showcase
- Hardware Setup
- Other code written for this project
  - iOS App (Swift)
  - MQTT to Core MIDI (Python)
  - MQTT Video Trigger (Processing)
  - Leaderboard (Processing)

### Installation
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
