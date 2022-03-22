var util = require('util');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'On / Off';

var LampiOnOffCharacteristic = function(lampiState) {
  LampiOnOffCharacteristic.super_.call(this, {
    uuid: '0004A7D3-D8A4-4FEA-8174-1736E808C066',
    properties: ['read', 'write', 'notify'],
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

  this.changed_onoff = function(is_on) {
    console.log('lampiState changed LampiOnOffCharacteristic');
    if( this._update !== null ) {
        console.log('this._update is ', typeof(this._update));
        console.log('updating new onoff uuid=', this.uuid);
        var data = new Buffer(1);
        if (is_on) {
            data.writeUInt8(0x01, 0);
        } else {
            data.writeUInt8(0x0, 0);
        }
        this._update(data);
    }
  }

  this.lampiState = lampiState;

  this.lampiState.on('changed-onoff', this.changed_onoff.bind(this));

}

util.inherits(LampiOnOffCharacteristic, bleno.Characteristic);

LampiOnOffCharacteristic.prototype.onReadRequest = function(offset, callback) {
  console.log('onReadRequest');
  if (offset) {
    console.log('onReadRequest offset');
    callback(this.RESULT_ATTR_NOT_LONG, null);
  }
  else {
    var data = new Buffer(1);
    if (this.lampiState.is_on) {
        data.writeUInt8(0x01, 0);
    } else {
        data.writeUInt8(0x0, 0);
    }
    console.log('onReadRequest returning ', data);
    callback(this.RESULT_SUCCESS, data);
  }
};

LampiOnOffCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
    if(offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 1) {
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
        var new_onoff = data.readUInt8(0);
        this.lampiState.set_onoff( new_onoff === 0x1);
        callback(this.RESULT_SUCCESS);
    }
};

LampiOnOffCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
    console.log('subscribe on ', CHARACTERISTIC_NAME);
    this._update = updateValueCallback;
}

LampiOnOffCharacteristic.prototype.onUnsubscribe = function() {
    console.log('unsubscribe on ', CHARACTERISTIC_NAME);
    this._update = null;
}

module.exports = LampiOnOffCharacteristic;

