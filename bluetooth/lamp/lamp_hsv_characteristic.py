from pybleno import *
import array

CHARACTERISTIC_NAME = "HSV"


def build_hsv_buffer(h, s, v):
    data = array.array('B', [0] * 3)
    writeUInt8(data, round(h), 0)
    writeUInt8(data, round(s), 1)
    writeUInt8(data, round(v), 2)
    return data


class HSVCharacteristic(Characteristic):
    def __init__(self, lamp_state):
        Characteristic.__init__(self, {
            'uuid': '0002A7D3-D8A4-4FEA-8174-1736E808C066',
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
        self._update_value_callback = None

    # TODO: setup lampstate callback for the notify function

    def changed_hsv(self, hue, saturation, value):
        if self._update_value_callback is not None:
            data = build_hsv_buffer(hue, saturation, value)
            self._update_value_callback(data)

    def onReadRequest(self, offset, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            st = self._lamp_state
            data = build_hsv_buffer(st.hue, st.saturation, st.value)
            callback(Characteristic.RESULT_SUCCESS, data)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) != 3:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            hue = readUInt8(data, 0)
            saturation = readUInt8(data, 1)
            value = readUInt8(data, 2)
            self._lamp_state.set_hsv(hue, saturation, value)
            callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self.set_update_callback(updateValueCallback)

    def onUnsubscribe(self):
        self.set_update_callback(None)

    def set_update_callback(self, callback):
        self._update_value_callback = callback
        if callback is None:
            self._lamp_state.hsv_update_callback = None
        else:
            self._lamp_state.hsv_update_callback = self.changed_hsv
