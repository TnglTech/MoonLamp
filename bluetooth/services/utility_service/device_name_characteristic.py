from pybleno import *
import array

CHARACTERISTIC_NAME = "Device Name"

MIN_DEVICE_NAME_LENGTH = 1
MAX_DEVICE_NAME_LENGTH = 24


class DeviceNameCharacteristic(Characteristic):
    def __init__(self, utility_state):
        Characteristic.__init__(self, {
            'uuid': '1002A7D3-D8A4-4FEA-8174-1736E808C066',
            'properties': ['read', 'write'],
            'value': None,
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes(CHARACTERISTIC_NAME, 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x01, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })

        self._utility_state = utility_state

    def onReadRequest(self, offset, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            data = bytes(self._utility_state.device_name, 'utf-8')
            callback(Characteristic.RESULT_SUCCESS, data)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        else:
            name = data.decode("utf-8")
            if MIN_DEVICE_NAME_LENGTH <= len(name) <= MAX_DEVICE_NAME_LENGTH:
                self._utility_state.device_name = name
                callback(Characteristic.RESULT_SUCCESS)
            else:
                callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
