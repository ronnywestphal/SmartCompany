#!/usr/bin/python
import time
import datetime as dt
from typing import Counter

import paho.mqtt.client as mqtt
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projekt2.settings')
#django.setup()
from devices.models import *
from automation.views import receive_data

from django.apps import AppConfig
from threading import Thread

MQTT_ADDRESS = 'ronnysddns.hopto.org'
MQTT_USER = 'ateam'
MQTT_PASSWORD = 'ateam'
MQTT_TOPIC_SUB = 'home/+/+'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        print('Sub Connected with result code ' + str(rc))
        
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    
    return mqtt_client

def subscribe(client):
    global counter,payload,flag
    counter=payload=flag=0
    
    '''while flag==0:
        def on_message(client, userdata, msg):
            counter += 1
            
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")##
            #sector_only_consumption(msg.topic, msg.payload.decode())
            payload += decimal.Decimal(msg.payload.decode())
            if dt.datetime.now().second == time(0).second:    
                receive_data(msg.topic, payload)
                flag+=1'''
    
    def on_message(client, userdata, msg):            
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")##
        #sector_only_consumption(msg.topic, msg.payload.decode())
        #print("received topic: {}.".format(msg.topic))
        receive_data(msg.topic, msg.payload.decode())
    client.subscribe(MQTT_TOPIC_SUB)
    client.on_message = on_message
        
    
def main():
    global counter
    counter=0
    
    client = connect_mqtt()

    client.loop_start()
    
    while True:
        time.sleep(1)
        #print('listening')
        subscribe(client)


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()