var util = require('util');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'HSV';

function LampiHSVCharacteristic(lampiState) {
  LampiHSVCharacteristic.super_.call(this, {
    uuid: '0002A7D3-D8A4-4FEA-8174-1736E808C066',
    properties: ['read', 'write', 'notify'],
    secure: [],
    descriptors: [
        new bleno.Descriptor({
            uuid: '2901',
            value: CHARACTERISTIC_NAME,
        }),
        new bleno.Descriptor({
           uuid: '2904',
           value: new Buffer([0x07, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
        }),
    ],
  });

  this._update = null;

  this.changed_hsv =  function(h, s, v) {
    console.log('lampiState changed LampiHSVCharacteristic');
    if( this._update !== null ) {
        var data = new Buffer([h, s, v]);
        this._update(data);
    } 
  }

  this.lampiState = lampiState;

  this.lampiState.on('changed-hsv', this.changed_hsv.bind(this));

}

util.inherits(LampiHSVCharacteristic, bleno.Characteristic);

LampiHSVCharacteristic.prototype.onReadRequest = function(offset, callback) {
  console.log('onReadRequest');
  if (offset) {
    console.log('onReadRequest offset');
    callback(this.RESULT_ATTR_NOT_LONG, null);
  }
  else {
    var data = new Buffer(3);
    data.writeUInt8(Math.round(this.lampiState.hue), 0);
    data.writeUInt8(Math.round(this.lampiState.saturation), 1);
    data.writeUInt8(Math.round(this.lampiState.value), 2);
    console.log('onReadRequest returning ', data);
    callback(this.RESULT_SUCCESS, data);
  }
};

LampiHSVCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
    console.log('onWriteRequest');
    if(offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 3) {
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
        var hue = data.readUInt8(0);
        var saturation = data.readUInt8(1);
        var value = data.readUInt8(2);
        this.lampiState.set_hsv( hue, saturation, value );
        callback(this.RESULT_SUCCESS);
    }
};

LampiHSVCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
    console.log('subscribe on ', CHARACTERISTIC_NAME);
    this._update = updateValueCallback;
}

LampiHSVCharacteristic.prototype.onUnsubscribe = function() {
    console.log('unsubscribe on ', CHARACTERISTIC_NAME);
    this._update = null;
}

module.exports = LampiHSVCharacteristic;

