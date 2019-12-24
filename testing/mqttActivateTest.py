import paho.mqtt.client as mqtt
from gpiozero import LED
from time import sleep

laser = LED(23)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("lasermaze")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if(str(msg.payload)=="1"):
		print("Laser on.")
		laser.on()
	elif (str(msg.payload)=="0"):
		print("Laser off.")
		laser.off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.236", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
client.loop_forever()
