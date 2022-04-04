from pybleno import *
import array

CHARACTERISTIC_NAME = "Association Code"


class IsAssociatedCharacteristic(Characteristic):
    def __init__(self, association_state):
        Characteristic.__init__(self, {
            'uuid': '2003A7D3-D8A4-4FEA-8174-1736E808C066',
            'properties': ['read', 'notify'],
            'value': None,
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes(CHARACTERISTIC_NAME, 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })

        self._assoc_state = association_state
