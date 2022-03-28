from pybleno import *


class UtilityService(BlenoPrimaryService):
    uuid = "1001A7D3-D8A4-4FEA-8174-1736E808C066"

    def __init__(self, utility_state):
        self._utility_state = utility_state
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [

            ]
        })
