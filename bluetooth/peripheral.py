#!/usr/bin/env python3

from pybleno import *
import sys
import signal
from lamp.lamp_service import LampService
from device_info_service import DeviceInfoService
from lamp.lamp_state import LampState
import paho.mqtt.client as mqtt
import os
import json

DEVICE_ID_FILENAME = '/sys/class/net/wlan0/address'
TOPIC_BLUETOOTH = 'lamp/bluetooth'


def get_device_id():
    mac_addr = open(DEVICE_ID_FILENAME).read().strip()
    return mac_addr.replace(':', '')


os.environ["BLENO_DEVICE_NAME"] = "MOONLAMP - " + get_device_id()

bleno = Bleno()

lamp_state = LampState()
lamp_service = LampService(lamp_state)
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
        bleno.startAdvertising('MoonLamp', [lamp_service.uuid, device_info_service.uuid])
    else:
        bleno.stopAdvertising()


bleno.on('stateChange', onStateChange)


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        def on_setServiceError(error):
            print('setServices: %s' % ('error ' + error if error else 'success'))

        bleno.setServices([
            lamp_service,
            device_info_service
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
