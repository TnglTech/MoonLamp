from pybleno import *
from .lamp_onoff_characteristic import OnOffCharacteristic
from .lamp_brightness_characteristic import BrightnessCharacteristic
from .lamp_hsv_characteristic import HSVCharacteristic


class LampService(BlenoPrimaryService):
    uuid = '0001A7D3-D8A4-4FEA-8174-1736E808C066'

    def __init__(self, lamp_state):
        self._lamp_state = lamp_state
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [
                HSVCharacteristic(self._lamp_state),
                BrightnessCharacteristic(self._lamp_state),
                OnOffCharacteristic(self._lamp_state)
            ]
        })
