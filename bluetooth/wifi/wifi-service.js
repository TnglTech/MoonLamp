var util = require('util');
var bleno = require('bleno');

var WifiState = require('./wifi-state');

var WifiSSIDCharacteristic = require('./wifi-ssid-characteristic');
var WifiPSKCharacteristic = require('./wifi-psk-characteristic');
var WifiUpdateCharacteristic = require('./wifi-update-characteristic');

function WifiService() {
    var wifiState = new WifiState();
    bleno.PrimaryService.call(this, {
        uuid: '08c7042c-12da-49e8-845e-6086d18a81fa',
        characteristics: [
            new WifiSSIDCharacteristic(wifiState),
            new WifiPSKCharacteristic(wifiState),
            new WifiUpdateCharacteristic(wifiState),
        ],
    });
}

util.inherits(WifiService, bleno.PrimaryService);

module.exports = WifiService;