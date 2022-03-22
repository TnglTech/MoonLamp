var util = require('util');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'PSK';

var WifiPskCharacteristic = function(wifiState) {
    WifiPskCharacteristic.super_.call(this, {
        uuid: '28c7042c-12da-49e8-845e-6086d18a81fa',
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

util.inherits(WifiPskCharacteristic, bleno.Characteristic);

WifiPskCharacteristic.prototype.onReadRequest = function(offset, callback) {
    console.log('onReadRequest');
    if (offset) {
        console.log('onReadRequest offset');
        callback(this.RESULT_ATTR_NOT_LONG, null);
    } else {
        let responseData = new Buffer(this.wifiState.psk);
        console.log("onReadRequest returning ", responseData);
        callback(this.RESULT_SUCCESS, responseData);
    }
}

WifiPskCharacteristic.prototype.onWriteRequest = function(data, offset, withoutRespose, callback) {
    console.log("hit write request")
    if (offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    } else if (data.length < 0) {
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    } else if (data.length == 0) {
        console.log("0 data length");
        this.wifiState.set_psk("");
        callback(this.RESULT_SUCCESS);
    } else {
        let str = data.toString();
        this.wifiState.set_psk(str);
        console.log(data.toString());
        callback(this.RESULT_SUCCESS);
    }
}

module.exports = WifiPskCharacteristic;