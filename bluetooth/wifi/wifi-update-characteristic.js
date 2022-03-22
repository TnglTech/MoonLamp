var util = require('util');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'Update Credentials';

var WifiUpdateCharacteristic = function(wifiState) {
    WifiUpdateCharacteristic.super_.call(this, {
        uuid: '38c7042c-12da-49e8-845e-6086d18a81fa',
        properties: ['write', 'notify'],
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

    this.received_update_response = function(status) {
        console.log('received response');
        if ( this._update !== null ) {
            console.log('this._update is ', typeof(this._update));
            var data = new Buffer(1);
            if (status) {
                data.writeUInt8(0x01, 0);
            } else {
                data.writeUInt8(0x00, 0);
            }
            this._update(data);
        }
    }

    this.wifiState.on('received-update-response', this.received_update_response.bind(this))
}

util.inherits(WifiUpdateCharacteristic, bleno.Characteristic);

/*WifiUpdateCharacteristic.prototype.onReadRequest = function(offset, callback) {
    console.log('onReadRequest');
    if (offset) {
        console.log('onReadRequest offset');
        callback(this.RESULT_ATTR_NOT_LONG, null);
    } else {
        var responseData = new Buffer(1);;
        if (this.wifiState.last_attempt) {
            responseData.writeUInt8(0x01, 0);
        } else {
            responseData.writeUInt8(0x00, 0);
        }
        console.log("onReadRequest returning ", responseData);
        callback(this.RESULT_SUCCESS, responseData);
    }
}*/

WifiUpdateCharacteristic.prototype.onWriteRequest = function(data, offset, withoutRespose, callback) {
    if (offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    } else if (data.length <= 0) {
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    } else {
        var new_state = data.readUInt8(0);
        console.log(data.toString());

        let result = this.wifiState.join_wifi();
        /*if ( this._update !== null ) {
            var data = new Buffer(1);
            console.log("updating with result ", result);
            if (result) {
                data.writeUInt8(0x01, 0);
            } else {
                data.writeUInt8(0x00, 0);
            }
            this._update(data);
        }*/

        callback(this.RESULT_SUCCESS);
    }
}

WifiUpdateCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
    console.log('subscribe on ', CHARACTERISTIC_NAME);
    this._update = updateValueCallback;
}

WifiUpdateCharacteristic.prototype.onUnsubscribe = function() {
    console.log('unsubscribe on ', CHARACTERISTIC_NAME);
    this._update = null;
}

module.exports = WifiUpdateCharacteristic;