/*
    Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleServer.cpp
    Ported to Arduino ESP32 by Evandro Copercini
    updates by chegewara
*/
#include "EspMQTTClient.h"
//#include "ArduinoJson.h"
#include "LampState.h"
#include "LampDriver.h"
#include "BLE.h"

LampState *lamp_state = new LampState();
LampDriver *driver = new LampDriver(lamp_state);
BLE *ble;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE work!");
  Serial.println(ESP.getEfuseMac());

  ble = new BLE(lamp_state);
//  uint8_t tp = 125;
  ble->hsvCharacteristic->setHSV(255,255);
  ble->brightnessCharacteristic->setBrightness(125);
  
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(DEVICE_INFO_SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now you can read it in your phone!");
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(2000);
}
