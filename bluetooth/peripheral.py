#!/usr/bin/env python3

from pybleno import *
import sys
import signal
from helper import Helper
from utility.utility_state import UtilityState
from lamp.lamp_state import LampState
from wifi.wifi_state import WifiState
from utility.utility_service import UtilityService
from lamp.lamp_service import LampService
from wifi.wifi_service import WifiService
from device_info_service import DeviceInfoService
import paho.mqtt.client as mqtt
import os
import json

TOPIC_BLUETOOTH = 'lamp/bluetooth'

helper = Helper()

os.environ["BLENO_DEVICE_NAME"] = "MOONLAMP - " + Helper.get_device_id()

bleno = Bleno()

utility_state = UtilityState(helper)
utility_service = UtilityService(utility_state)

lamp_state = LampState(helper)
lamp_service = LampService(lamp_state)

wifi_state = WifiState(helper)
wifi_service = WifiService(wifi_state)

device_info_service = DeviceInfoService('MoonLamp', 'ML_0001', '000001')

MQTT_CLIENT_ID = 'lamp_bt_central'
MQTT_VERSION = mqtt.MQTTv311
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_BROKER_KEEP_ALIVE_SECS = 60
mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=MQTT_VERSION)
mqtt_client.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)

bt_clientAddress = None
bt_lastRssi = 0


def onStateChange(state):
    print("New state: " + state);

    if (state == 'poweredOn'):
        bleno.startAdvertising('MoonLamp', [utility_service.uuid, device_info_service.uuid])
    else:
        bleno.stopAdvertising()


bleno.on('stateChange', onStateChange)


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        def on_setServiceError(error):
            print('setServices: %s' % ('error ' + error if error else 'success'))

        bleno.setServices([
            utility_service,
            device_info_service,
            lamp_service
        ], on_setServiceError)


bleno.on('advertisingStart', onAdvertisingStart)


def updateRSSI(rssi):
    global bt_clientAddress, bt_lastRssi
    if bt_clientAddress:
        if abs(rssi - bt_lastRssi) > 2:
            mqtt_client.publish(TOPIC_BLUETOOTH, json.dumps({
                'client': bt_clientAddress,
                'rssi': rssi
            }))

        bt_lastRssi = rssi



def onAccept(clientAddress):
    global bt_clientAddress, bt_lastRssi
    bt_clientAddress = clientAddress
    bt_lastRssi = 0
    mqtt_client.publish(TOPIC_BLUETOOTH, json.dumps({
        'state': 'connected',
        'client': bt_clientAddress
    }))

    bleno.updateRssi(updateRSSI)

#bleno.on('accept', onAccept)


def onDisconnect(clientAddress):
    global bt_clientAddress, bt_lastRssi
    mqtt_client.publish(TOPIC_BLUETOOTH, json.dumps({
        'state': 'disconnected',
        'client': bt_clientAddress
    }))
    bt_clientAddress = None
    bt_lastRssi = 0


#bleno.on('disconnect', onDisconnect)

bleno.start()

try:
    while True:
        pass
except Exception:
    pass

bleno.stopAdvertising()
bleno.disconnect()

print('terminated.')
sys.exit(1)
