from pybleno import *
import array

CHARACTERISTIC_NAME = "HSV""


class OnOffCharacteristic(Characteristic):
    def __init__(self, lamp_state):
        Characteristic.__init__(self, {
            'uuid': '0004A7D3-D8A4-4FEA-8174-1736E808C067',
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

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) != 1:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            new_onoff = readUInt8(data, 0)
            self._lamp_state.set_onoff(new_onoff == 0x01)
            callback(Characteristic.RESULT_SUCCESS)

    def onReadRequest(self, offset, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            data = array.array('B', [0] * 1)
            if self._lamp_state.is_on:
                writeUInt8(data, 0x01, 0)
            else:
                writeUInt8(data, 0x00, 0)
            callback(Characteristic.RESULT_SUCCESS, data)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        self._updateValueCallback = None;