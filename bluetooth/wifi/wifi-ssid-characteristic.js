var util = require('util');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'SSID';

var WifiSsidCharacteristic = function(wifiState) {
    WifiSsidCharacteristic.super_.call(this, {
        uuid: '18c7042c-12da-49e8-845e-6086d18a81fa',
        properties: ['read', 'write'],
        secure: [],
        descriptors: [
            new bleno.Descriptor({
                uuid: '2901',
                value: CHARACTERISTIC_NAME,
            }),
            new bleno.Descriptor({
                uuid: '2904',
                value: new Buffer([0x04, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
            }),
        ],
    });

    this._update = null;

    this.wifiState = wifiState;

}

util.inherits(WifiSsidCharacteristic, bleno.Characteristic);

WifiSsidCharacteristic.prototype.onReadRequest = function(offset, callback) {
    console.log('onReadRequest');
    if (offset) {
        console.log('onReadRequest offset');
        callback(this.RESULT_ATTR_NOT_LONG, null);
    } else {
        let responseData = new Buffer(this.wifiState.ssid);
        console.log("onReadRequest returning ", responseData);
        callback(this.RESULT_SUCCESS, responseData);
    }
}

WifiSsidCharacteristic.prototype.onWriteRequest = function(data, offset, withoutRespose, callback) {
    if (offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    } else if (data.length <= 0) {
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    } else {
        let str = data.toString();
        this.wifiState.set_ssid(str);
        console.log(data.toString());
        callback(this.RESULT_SUCCESS);
    }
}

module.exports = WifiSsidCharacteristic;