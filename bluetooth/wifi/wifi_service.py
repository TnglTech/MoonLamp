from pybleno import *
from .wifi_ssid_characteristic import SSIDCharacteristic
from .wifi_psk_characteristic import PSKCharacteristic
from .wifi_update_characteristic import WiFiUpdateCharacteristic
from .wifi_feedback_characteristic import WiFiFeedbackCharacteristic


class WifiService(BlenoPrimaryService):
    uuid = "3001A7D3-D8A4-4FEA-8174-1736E808C066"

    def __init__(self, wifi_state):
        self._wifi_state = wifi_state
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [
                SSIDCharacteristic(wifi_state),
                PSKCharacteristic(wifi_state),
                WiFiUpdateCharacteristic(wifi_state),
                WiFiFeedbackCharacteristic(wifi_state),
            ]
        })
        print("Started WiFi Service")
