from pybleno import *
import array

CHARACTERISTIC_NAME = "Update Wifi"


class WiFiUpdateCharacteristic(Characteristic):
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
        self._update_value_callback = None

    def send_notification(self, value):
        if self._update_value_callback is not None:
            data = array.array('B', [0] * 1)
            writeUInt8(data, value, 0)
            self._update_value_callback(data)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) <= 0:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            val = readUInt8(data, 0)
            self._wifi_state.join_wifi()
            callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self.set_update_callback(updateValueCallback)

    def onUnsubscribe(self):
        self.set_update_callback(None)

    def set_update_callback(self, callback):
        self._update_value_callback = callback
        if callback is not None:
            self._wifi_state.update_action_callback = self.send_notification
        else:
            self._wifi_state.update_action_callback = None
