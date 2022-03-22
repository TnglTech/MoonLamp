var util = require('util');
var bleno = require('bleno');

var LampOnOffCharacteristic = require('./lamp-onoff-characteristic');
var LampBrightnessCharacteristic = require('./lamp-brightness-characteristic');
var LampHSVCharacteristic = require('./lamp-hsv-characteristic');

function LampService(lampState) {
    bleno.PrimaryService.call(this, {
        uuid: '0001A7D3-D8A4-4FEA-8174-1736E808C066',
        characteristics: [
            new LampHSVCharacteristic(lampState),
            new LampBrightnessCharacteristic(lampState),
            new LampOnOffCharacteristic(lampState),
        ]
    });
}

util.inherits(LampService, bleno.PrimaryService);

module.exports = LampService;
