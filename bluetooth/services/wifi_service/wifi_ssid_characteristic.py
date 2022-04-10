from pybleno import *
import array

CHARACTERISTIC_NAME = "SSID"


class SSIDCharacteristic(Characteristic):
    def __init__(self, wifi_state):
        Characteristic.__init__(self, {
            'uuid': '3002A7D3-D8A4-4FEA-8174-1736E808C066',
            'properties': ['read', 'write'],
            'value': None,
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes(CHARACTERISTIC_NAME, 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })

        self._wifi_state = wifi_state

    def onReadRequest(self, offset, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            data = bytes(self._wifi_state.ssid, 'utf-8')
            callback(Characteristic.RESULT_SUCCESS, data)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) <= 0:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            ssid = data.decode("utf-8")
            self._wifi_state.set_ssid(ssid)
            callback(Characteristic.RESULT_SUCCESS)

