#! /usr/bin/env node
var child_process = require('child_process');
var device_id = child_process.execSync('cat /sys/class/net/eth0/address | sed s/://g').toString().replace(/\n$/, '');

process.env['BLENO_DEVICE_NAME'] = 'LAMPI ' + device_id;

var serviceName = 'LampiService';
var bleno = require('bleno');
var mqtt = require('mqtt');
 
var LampiState = require('./lamp/lampi-state');
var LampiService = require('./lamp/lampi-service');
var DeviceInfoService = require('./device-info-service');
var WifiService = require('./wifi/wifi-service');

var lampiState = new LampiState();
var lampiService = new LampiService( lampiState );
var deviceInfoService = new DeviceInfoService( 'CWRU', 'LAMPI', device_id);
var wifiService = new WifiService();

var bt_clientAddress = null;
var bt_lastRssi = 0;

var mqtt_clientId = 'lamp_bt_central';
var mqtt_client_connection_topic = 'lamp/connection/' + mqtt_clientId + '/state';

var mqtt_options = {
    clientId: mqtt_clientId,
}

var mqtt_client = mqtt.connect('mqtt://localhost', mqtt_options);


bleno.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    //
    // We will also advertise the service ID in the advertising packet,
    // so it's easier to find.
    //
    bleno.startAdvertising('LampiService', [lampiService.uuid, deviceInfoService.uuid], function(err)  {
      if (err) {
        console.log(err);
      }
    });
  }
  else {
    bleno.stopAdvertising();
    console.log('not poweredOn');
  }
});


bleno.on('advertisingStart', function(err) {
  if (!err) {
    console.log('advertising...');
    //
    // Once we are advertising, it's time to set up our services,
    // along with our characteristics.
    //
    bleno.setServices([
        lampiService,
        wifiService,
        deviceInfoService,
    ]);
  }
});

function updateRSSI(err, rssi) {
    // if we are still connected
    if (bt_clientAddress) {
        // and large change in RSSI
        if ( Math.abs(rssi - bt_lastRssi) > 2 ) {
            // publish RSSI value to MQTT 
            mqtt_client.publish('lamp/bluetooth', JSON.stringify({
                'client': bt_clientAddress,
                'rssi': rssi,
                }));
        }
        // update our last RSSI value
        bt_lastRssi = rssi;
        // set a timer to update RSSI again in 1 second
        setTimeout( function() {
            bleno.updateRssi( updateRSSI );
            }, 1000);
        }
}


bleno.on('accept', function(clientAddress) {
    console.log('accept: ' + clientAddress);
    bt_clientAddress = clientAddress;    
    bt_lastRssi = 0;
    mqtt_client.publish('lamp/bluetooth', JSON.stringify({
        state: 'connected',
        'client': bt_clientAddress,
        }));

    bleno.updateRssi( updateRSSI );
});

bleno.on('disconnect', function(clientAddress) {
    console.log('disconnect: ' + clientAddress);
    mqtt_client.publish('lamp/bluetooth', JSON.stringify({
        state: 'disconnected',
        'client': bt_clientAddress,
        }));
    bt_clientAddress = null;
    bt_lastRssi = 0;
});

