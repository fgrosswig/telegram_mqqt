#!/usr/bin/python3

#
# require settings.conf
#
# structure >>>
# [TELEGRAM]
# bot_token = 
# chat_id = 
# 
# [MQTT]
# SERVER_IP = 127.0.0.1
# SERVER_PORT = 1883

import paho.mqtt.client as mqtt
import sys
import json
import telepot
import time
from configparser import ConfigParser
from telepot.loop import MessageLoop
import requests
import pytest

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("frontdoor/cam/0/movie_end")

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    json_obj=json.loads(msg.payload)
    if "filename" in json_obj:
        result=json_obj["filename"]
        #bot.sendPhoto(bot_chatID, photo=open(result, 'rb'), caption=result)
        if result.endswith(".mp4"):         
            bot.sendVideo(bot_chatID, video=open(result, 'rb'), caption=result)

    else:
        print("No filename, skipping")


def main(argv=None):
    global bot_token
    global bot_chatID
    global bot

    config_object = ConfigParser()
    config_object.read('./settings.conf')

    bot_token = config_object["TELEGRAM"]["BOT_TOKEN"]
    bot_chatID = config_object["TELEGRAM"]["CHAT_ID"]
    bot = telepot.Bot(bot_token)



    global client
    client = mqtt.Client("movie_save_listener")  # Create instance of client with client ID “digi_mqtt_test”
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.connect(config_object["MQTT"]["SERVER_IP"], int(config_object["MQTT"]["SERVER_PORT"]))
    client.loop_forever()  # Start networking daemon

if __name__ == "__main__":
    main()

