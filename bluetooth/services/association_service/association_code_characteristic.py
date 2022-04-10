from pybleno import *
import array

CHARACTERISTIC_NAME = "Association Code"


class AssociationCodeCharacteristic(Characteristic):
    def __init__(self, association_state):
        Characteristic.__init__(self, {
            'uuid': '2002A7D3-D8A4-4FEA-8174-1736E808C066',
            'properties': ['read', 'notify'],
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

        self._assoc_state = association_state
        self._update_value_callback = None

    def send_association_code(self, code):
        if self._update_value_callback is not None:
            data = bytes(code, 'utf-8')
            self._update_value_callback(data)

    def onReadRequest(self, offset, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        else:
            data = bytes(self._assoc_state.association_code, 'utf-8')
            callback(Characteristic.RESULT_SUCCESS, data)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self.set_update_callback(updateValueCallback)

    def onUnsubscribe(self):
        self.set_update_callback(None)

    def set_update_callback(self, callback):
        self._update_value_callback = callback
        if callback is not None:
            self._assoc_state.association_code_callback = self.send_association_code
        else:
            self._assoc_state.association_code_callback = None

