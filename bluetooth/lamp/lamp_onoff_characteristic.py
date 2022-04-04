from pybleno import *
import array

CHARACTERISTIC_NAME = "On / Off"


def build_onoff_buffer(is_on):
    data = array.array('B', [0] * 1)
    if is_on:
        writeUInt8(data, 0x01, 0)
    else:
        writeUInt8(data, 0x00, 0)
    return data


class OnOffCharacteristic(Characteristic):
    def __init__(self, lamp_state):
        Characteristic.__init__(self, {
            'uuid': '0004A7D3-D8A4-4FEA-8174-1736E808C066',
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

    def changed_onoff(self, is_on):
        if self._update_value_callback is not None:
            data = build_onoff_buffer(is_on)
            self._update_value_callback(data)

    def onReadRequest(self, offset, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            data = build_onoff_buffer(self._lamp_state.is_on)
            callback(Characteristic.RESULT_SUCCESS, data)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) != 1:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            new_onoff = readUInt8(data, 0)
            self._lamp_state.set_onoff(new_onoff == 0x01)
            callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self.set_update_callback(updateValueCallback)

    def onUnsubscribe(self):
        self.set_update_callback(None)

    def set_update_callback(self, callback):
        self._update_value_callback = callback
        if callback is None:
            self._lamp_state.onoff_update_callback = None
        else:
            self._lamp_state.onoff_update_callback = self.changed_onoff
