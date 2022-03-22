var util = require('util');
var bleno = require('bleno');

var ManufacturerCharacteristic = function(manufacturer) {
    bleno.Characteristic.call(this, {
        uuid: '2A29',
        properties: ['read'],
        descriptors: [
            new bleno.Descriptor({
               uuid: '2901',
               value: 'Manufacturer Name'
            }),
            new bleno.Descriptor({
               uuid: '2904',
               value: new Buffer([0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
            }),
        ],
        value: new Buffer(manufacturer),
    }
    )
}

util.inherits(ManufacturerCharacteristic, bleno.Characteristic);

var ModelCharacteristic = function(model) {
    bleno.Characteristic.call(this, {
        uuid: '2A24',
        properties: ['read'],
        descriptors: [
            new bleno.Descriptor({
               uuid: '2901',
               value: 'Model Number'
            }),
            new bleno.Descriptor({
               uuid: '2904',
               value: new Buffer([0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
            }),
        ],
        value: new Buffer(model),
    }
    )
}

util.inherits(ModelCharacteristic, bleno.Characteristic);

var SerialCharacteristic = function(serial) {
    bleno.Characteristic.call(this, {
        uuid: '2A25',
        properties: ['read'],
        descriptors: [
            new bleno.Descriptor({
               uuid: '2901',
               value: 'Serial Number'
            }),
            new bleno.Descriptor({
               uuid: '2904',
               value: new Buffer([0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
            }),
        ],
        value: new Buffer(serial),
    }
    )
}

util.inherits(SerialCharacteristic, bleno.Characteristic);

function DeviceInfoService(manufacturer, model, serial) {
    bleno.PrimaryService.call(this, {
        uuid: '180a',
        characteristics: [
            new ManufacturerCharacteristic(manufacturer),
            new ModelCharacteristic(model),
            new SerialCharacteristic(serial),
        ]
    });
}

util.inherits(DeviceInfoService, bleno.PrimaryService);

module.exports = DeviceInfoService;
