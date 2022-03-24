from pybleno import *
import array

CHARACTERISTIC_NAME = "Brightness"


def build_brightness_buffer(brightness):
    data = array.array('B', [0] * 1)
    writeUInt8(data, round(brightness), 0)
    return data


class BrightnessCharacteristic(Characteristic):
    def __init__(self, lamp_state):
        Characteristic.__init__(self, {
            'uuid': '0003A7D3-D8A4-4FEA-8174-1736E808C066',
            'properties': ['read', 'write', 'notify'],
            'value': None,
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes(CHARACTERISTIC_NAME, 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x04, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })

        self._lamp_state = lamp_state
        self._updateValueCallback = None

        # TODO: setup lampstate callback for the notify function

    def changed_brightness(self, is_on):
        if self._updateValueCallback is not None:
            data = build_brightness_buffer(is_on)
            self._updateValueCallback(data)

    def onReadRequest(self, offset, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            data = build_brightness_buffer(self._lamp_state.brightness)
            callback(Characteristic.RESULT_SUCCESS, data)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) != 1:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            brightness = readUInt8(data, 0)
            self._lamp_state.set_brightness(brightness)
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
