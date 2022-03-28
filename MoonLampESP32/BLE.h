#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include "LampCharacteristics.h"


#define UTILITY_SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define NAME_CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

#define LAMP_SERVICE_UUID        "0001A7D3-D8A4-4FEA-8174-1736E808C066"


#define DEVICE_INFO_SERVICE_UUID "180a"
#define MANUFACTURER_CH_UUID "2a29"
#define MODEL_CH_UUID "2a24"
#define SERIAL_CH_UUID "2a25"

/**
 * 
 */
class BLE {
  public:
    BLEServer *server;
    std::string deviceID;

    BLEService *deviceInfoService;
    BLECharacteristic *manufacturerCharacteristic;
    BLECharacteristic *modelCharacteristic;
    BLECharacteristic *serialCharacteristic;
    

    BLEService *utilityService;
    BLECharacteristic *nameCharacteristic;
    
    BLEService *lampService;
    HSVCharacteristic *hsvCharacteristic;
    BrightnessCharacteristic *brightnessCharacteristic;
    OnOffCharacteristic *onOffCharacteristic;

    LampState *lampState;

    BLE(LampState* lampState) {
      this->lampState = lampState;
      
      deviceID = "abcd123";
      BLEDevice::init("MoonLamp");
      server = BLEDevice::createServer();

      setupDeviceInfoService();
      setupWifiService();
      setupAssociationService();
      setupLampService();
    }


  private:
    void setupDeviceInfoService() {
      deviceInfoService = server->createService(DEVICE_INFO_SERVICE_UUID);
      manufacturerCharacteristic = deviceInfoService->createCharacteristic(
                                                        MANUFACTURER_CH_UUID,
                                                        BLECharacteristic::PROPERTY_READ
                                                      );

      modelCharacteristic = deviceInfoService->createCharacteristic(
                                                        MODEL_CH_UUID,
                                                        BLECharacteristic::PROPERTY_READ
                                                      );
      serialCharacteristic = deviceInfoService->createCharacteristic(
                                                        SERIAL_CH_UUID,
                                                        BLECharacteristic::PROPERTY_READ
                                                      );

      manufacturerCharacteristic->setValue("MoonLamp Inc.");
      modelCharacteristic->setValue("MLD-0001");
      serialCharacteristic->setValue(deviceID);

      deviceInfoService->start();
    }

    void setupWifiService() {
      
    }

    void setupAssociationService() {
      
    }

    void setupLampService() {
      lampService = server->createService(LAMP_SERVICE_UUID);
      hsvCharacteristic = static_cast<HSVCharacteristic*>(lampService->createCharacteristic(
                                         HSV_CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       ));
      brightnessCharacteristic = static_cast<BrightnessCharacteristic*>(lampService->createCharacteristic(
                                         BRIGHTNESS_CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       ));
      onOffCharacteristic = static_cast<OnOffCharacteristic*>(lampService->createCharacteristic(
                                         ON_OFF_CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       ));

      lampService->start();
    }
  
};
