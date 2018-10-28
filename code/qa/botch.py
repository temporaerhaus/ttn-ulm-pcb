# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import gpiozero
# https://www.raspberrypi.org/documentation/usage/gpio/python/README.md

#import signal
import sys
from subprocess import run
import random
import string
from time import sleep
import json

from logger import Logger



### Config ###

debuggingActive = False
# import botch; from botch import *
boardCompile = False
boardFlash = False

boardId=7
mqttMessages = dict( [( str(boardId), [] )] )

ttnHandler = "eu.thethings.network"
ttnAppId = "ttn_ulm-muenstertest"
ttnAccessKey = "ttn-account-v2.FBY6xUTw1gAF9kpTla_UeYkWkVBXGYUihfaigMAYG-k"
ttnSubscribePath = "+/+/+/+"
# Test:
# mosquitto_sub -h eu.thethings.network -t '+/+/+/+' -u 'ttn_ulm-muenstertest' -P 'ttn-account-v2.FBY6xUTw1gAF9kpTla_UeYkWkVBXGYUihfaigMAYG-k'


logger = Logger()

mqttClient = None


### Functions ###


def mqttStartClient():
    global mqttClient

    # looks like we get random disconnects from other instances if this id  is not unique
    randomChars = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    mqttClient = mqtt.Client(client_id='client'+str(ttnAppId)+randomChars,
                         clean_session=False,
                         userdata=ttnAppId)

    mqttClient.on_connect = mqttOnConnect
    mqttClient.on_message = mqttOnMessage
    mqttClient.on_disconnect = mqttOnDisconnect
    if debuggingActive:
        mqttClient.on_log = mqttDebugLog

    mqttClient.username_pw_set(ttnAppId, ttnAccessKey)

    logger.log("Connecting to handler...")
    mqttClient.connect(ttnHandler, 1883, 60)

    logger.log("Starting MQTT loop asynchronously...")
    mqttClient.loop_start()


def mqttOnConnect(client, userdata, flags, rc):
    logger.log('Subscribing to app ' + ttnAppId + ' on topic ' + ttnSubscribePath + ' on handler ' + ttnHandler + "; connection returned result code: " + str(rc))
    client.subscribe(ttnSubscribePath)


def mqttOnDisconnect(client, userdata, rc):
    logger.log("Disconnected from Handler", "ERROR")
    if rc != 0:
        logger.log('Unexcepted disconnect from app ' + str(userdata) + '. Reason: ' + str(rc), 'RECONNECT')
        logger.log('Retrying connection...', 'RECONNECT')
        client.connect(ttnHandler, 1883, 60)


def mqttOnMessage(client, userdata, msg):
    global mqttMessages
    global testState

    logger.log('Message on topic "' + str(msg.topic) + '" received.')
    if debuggingActive:
        logger.log('Message:\n"' + str(msg.payload), 'DEBUG-MSG')

    testState = 0
    mqttMessages[str(boardId)].append({'topic': msg.topic, 'payload': json.loads(msg.payload.decode('utf8').replace("'", '"'))})
    #logger.log('Message queued.')

    # Info: https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format/40060181
    #  logger.log(json.dumps(mqttMessages[str(boardId)]['payload'], indent=4, sort_keys=True), 'DEBUG-MSG')
    #  logger.log(mqttMessages[str(boardId)]['payload'], 'DEBUG-MSG')




def mqttDebugLog(client, userdata, level, buf):
    global state
    logger.log(str(buf), 'DEBUG-MQTT')


def arduinoFlash():
    if boardCompile:
        logger.log('Compiling Arduino sketch:')
        run(["arduino-cli", "compile", "--fqbn", "arduino:avr:pro:cpu=8MHzatmega328", "testroutine-board"])
    if boardFlash:
        logger.log('Falshing firmware to board:')
        run(["arduino-cli", "upload", "--port", "/dev/ttyUSB0", "--fqbn", "arduino:avr:pro:cpu=8MHzatmega328", "testroutine-board"])


def checkInput():
    return


def checkOutput():
    return



### Main ###


mqttStartClient()

arduinoFlash()

testState = 1
while testState == 1:
    print('.')
    sleep(1)


print(mqttMessages[str(boardId)][0]['payload']['payload_fields'])

mqttClient.loop_stop()
mqttClient.disconnect()
