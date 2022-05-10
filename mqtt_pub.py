#!/usr/bin/python
from encodings import utf_8
import time
import random

import paho.mqtt.client as mqtt
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projekt2.settings')
django.setup()
from devices.models import *

MQTT_ADDRESS = 'ronnysddns.hopto.org'
MQTT_USER = 'ateam'
MQTT_PASSWORD = 'ateam'
MQTT_TOPIC_PUB = ['home/room1/fan', 'home/room1/led']


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server."""
        print('Pub Connected with result code ' + str(rc))
        
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    
    return mqtt_client

def publish_1(client):
    
    pl = Device.objects.all().order_by('sector')

    pl_list = []
    for x in pl:
        pl_list.append(getattr(x, 'power_level'))

    msg=[]
    for x in pl_list:
        msg.append(f"messages: {x}")
    
    for x,y in zip(msg,MQTT_TOPIC_PUB):
        client.publish(y, x) 
        print(f"Send `{x}` to topic `{y}`")

    
def main():
    client = connect_mqtt()
    client.loop_start()
    while True:
        time.sleep(2)
        publish_1(client)
    
if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()