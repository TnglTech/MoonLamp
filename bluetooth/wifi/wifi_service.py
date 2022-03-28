from pybleno import *


class WifiService(BlenoPrimaryService):
    uuid = "3001A7D3-D8A4-4FEA-8174-1736E808C066"

    def __init__(self, wifi_state):
        self._wifi_state = wifi_state
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [

            ]
        })
