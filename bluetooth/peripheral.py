from pybleno import *
import sys
import signal
from lamp.lamp_service import *
from lamp.lamp_state import LampState
import os

lamp_state = LampState()

DEVICE_ID_FILENAME = '/sys/class/net/wlan0/address'

def get_device_id():
    mac_addr = open(DEVICE_ID_FILENAME).read().strip()
    return mac_addr.replace(':', '')

os.environ["BLENO_DEVICE_NAME"] = "MOONLAMP - " + get_device_id()

bleno = Bleno()

primaryService = LampService(lamp_state);


def onStateChange(state):
    print('on -> stateChange: ' + state);

    if (state == 'poweredOn'):
        bleno.startAdvertising('Lampthing', [primaryService.uuid]);
    else:
        bleno.stopAdvertising();


bleno.on('stateChange', onStateChange)


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

    if not error:
        def on_setServiceError(error):
            print('setServices: %s' % ('error ' + error if error else 'success'))

        bleno.setServices([
            primaryService
        ], on_setServiceError)


bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

print('Hit <ENTER> to disconnect')

if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()

bleno.stopAdvertising()
bleno.disconnect()

print('terminated.')
sys.exit(1)

