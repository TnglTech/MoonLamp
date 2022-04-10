from pybleno import *
from .utility_state import UtilityState
from .device_name_characteristic import DeviceNameCharacteristic


class UtilityService(BlenoPrimaryService):
    uuid = "1001A7D3-D8A4-4FEA-8174-1736E808C066"

    def __init__(self, helper):
        self._utility_state = UtilityState(helper)
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [
                DeviceNameCharacteristic(self._utility_state)
            ]
        })
        print("Started Utility Service")
