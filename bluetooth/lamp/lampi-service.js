var util = require('util');
var bleno = require('bleno');

var LampiOnOffCharacteristic = require('./lampi-onoff-characteristic');
var LampiBrightnessCharacteristic = require('./lampi-brightness-characteristic');
var LampiHSVCharacteristic = require('./lampi-hsv-characteristic');

function LampiService(lampiState) {
    bleno.PrimaryService.call(this, {
        uuid: '0001A7D3-D8A4-4FEA-8174-1736E808C066',
        characteristics: [
            new LampiHSVCharacteristic(lampiState),
            new LampiBrightnessCharacteristic(lampiState),
            new LampiOnOffCharacteristic(lampiState),
        ]
    });
}

util.inherits(LampiService, bleno.PrimaryService);

module.exports = LampiService;
