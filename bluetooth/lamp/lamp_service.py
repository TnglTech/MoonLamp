from pybleno import *
from .lamp_onoff_characteristic import *


class LampService(BlenoPrimaryService):
    def __init__(self, lamp_state):
        self._lamp_state = lamp_state
        BlenoPrimaryService.__init__(self, {
            'uuid': 'ABCD',
            'characteristics': [
                OnOffCharacteristic(self._lamp_state),
            ]
        })