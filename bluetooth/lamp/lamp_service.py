from pybleno import *
from .lamp_onoff_characteristic import OnOffCharacteristic
from .lamp_brightness_characteristic import BrightnessCharacteristic
from .lamp_hsv_characteristic import HSVCharacteristic


class LampService(BlenoPrimaryService):
    def __init__(self, lamp_state):
        self._lamp_state = lamp_state
        BlenoPrimaryService.__init__(self, {
            'uuid': 'ABCD',
            'characteristics': [
                HSVCharacteristic(self._lamp_state),
                BrightnessCharacteristic(self._lamp_state),
                OnOffCharacteristic(self._lamp_state)
            ]
        })
