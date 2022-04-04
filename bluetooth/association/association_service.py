from pybleno import *
from .association_code_characteristic import AssociationCodeCharacteristic
from .is_associated_characteristic import IsAssociatedCharacteristic


class AssociationService(BlenoPrimaryService):
    uuid = "2001A7D3-D8A4-4FEA-8174-1736E808C066"

    def __init__(self, association_state):
        self._association_state = association_state
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [
                AssociationCodeCharacteristic(association_state)
            ]
        })
        print("Started Association Service")
