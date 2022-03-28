from pybleno import *
import array

CHARACTERISTIC_NAME = "Update Wifi"


class SSIDCharacteristic(Characteristic):
    def __init__(self, wifi_state):
        Characteristic.__init__(self, {
            'uuid': '3004A7D3-D8A4-4FEA-8174-1736E808C066',
            'properties': ['write', 'notify'],
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

        self._wifi_state = wifi_state
        self._updateValueCallback = None

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) <= 0:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            val = readUInt8(data, 0)
            result = self._wifi_state.join_wifi()
            callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self.set_update_callback(updateValueCallback)

    def onUnsubscribe(self):
        self.set_update_callback(None)

    def set_update_callback(self, callback):
        self._updateValueCallback = callback
        if callback is None:
            self._lamp_state.hsv_update_callback = None
        else:
            self._lamp_state.hsv_update_callback = self.changed_brightness
