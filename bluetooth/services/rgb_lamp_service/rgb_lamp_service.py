from pybleno import *
from .rgb_lamp_state import RgbLampState
from .rgb_lamp_onoff_characteristic import OnOffCharacteristic
from .rgb_lamp_brightness_characteristic import BrightnessCharacteristic
from .rgb_lamp_hsv_characteristic import HSVCharacteristic


class RgbLampService(BlenoPrimaryService):
    uuid = '0001A7D3-D8A4-4FEA-8174-1736E808C066'

    def __init__(self, helper):
        self._lamp_state = RgbLampState(helper)
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [
                HSVCharacteristic(self._lamp_state),
                BrightnessCharacteristic(self._lamp_state),
                OnOffCharacteristic(self._lamp_state)
            ]
        })
        print("Started Lamp Service")
