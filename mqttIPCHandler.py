#!/usr/bin/python3
import time
import paho.mqtt.client as mqtt
import json
from logger import Logger

class MqttIPC(object):
    mqtt_broker_priv = "127.0.0.1"
    mqtt_port = 1883
    mqtt_keep_alive = 60

    CLIENT_ID = "multivac_command"

    #Topics
    MQTT_TOPIC_CMD = "multivac/cmd"   #Topic for commands send/recv
    MQTT_TOPIC_SOUND = "multivac/feedback"   #Topic for commands send/recv

    #Connection Flag
    connected = False

    def __init__(self):
        self.Log = Logger("MqttIPC")
        self.Log.log("INIT")

        self.client = mqtt.Client(self.CLIENT_ID) #Creates unique ID

        # Register callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.Log.log("Connecting to broker at {}".format(self.mqtt_broker_priv))
        self.client.connect(self.mqtt_broker_priv, self.mqtt_port, self.mqtt_keep_alive)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        self.Log.log("Connection returned {}".format(rc))
        self.connected = True

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        self.Log.log("Client disconected - {}".format(rc))

    def send_camera(self, command):
        command_json = {
            "ID": self.CLIENT_ID,
            "CMD": command,
        }
        self.Log.log(json.dumps(command_json))
        self.client.publish(self.MQTT_TOPIC_CMD, json.dumps(command_json))
    def send_sound_off(self):
        command_json = {
            "ID": self.CLIENT_ID,
            "status": 0,
        }
        self.Log.log(json.dumps(command_json))
        self.client.publish(self.MQTT_TOPIC_SOUND, json.dumps(command_json))

    def is_connected(self):
        return self.connected

if __name__ == '__main__':
    pass