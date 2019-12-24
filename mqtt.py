import paho.mqtt.client as mqtt
from time import sleep
import game

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def send_msg(payload, topic = "videoCue"):
    publish(topic, payload, qos=0, retain=False)

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("Message: " ,msg)
    print("Topic = ",message.topic)
    game.accept_user_input(msg)


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.connect("192.168.1.133", 1883, 60) #Your MQTT broker IP address here.
client.subscribe("maze", 0)
client.loop_forever()
