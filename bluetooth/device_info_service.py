from pybleno import *


class ManufacturerCharacteristic(Characteristic):
    def __init__(self, manufacturer):
        Characteristic.__init__(self, {
            'uuid': '2A29',
            'properties': ['read'],
            'value': bytes(manufacturer, 'utf-8'),
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes('Manufacturer Name', 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })


class ModelCharacteristic(Characteristic):
    def __init__(self, model):
        Characteristic.__init__(self, {
            'uuid': '2A24',
            'properties': ['read'],
            'value': bytes(model, 'utf-8'),
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes('Model Number', 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })


class SerialCharacteristic(Characteristic):
    def __init__(self, serial):
        Characteristic.__init__(self, {
            'uuid': '2A25',
            'properties': ['read'],
            'value': bytes(serial, 'utf-8'),
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes('Serial Number', 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })


class DeviceInfoService(BlenoPrimaryService):
    uuid = '180a'

    def __init__(self, manufacturer, model, serial):
        BlenoPrimaryService.__init__(self, {
            'uuid': self.uuid,
            'characteristics': [
                ManufacturerCharacteristic(manufacturer),
                ModelCharacteristic(model),
                SerialCharacteristic(serial)
            ]
        })
