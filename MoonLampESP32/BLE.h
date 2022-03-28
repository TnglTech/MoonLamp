#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include "UtilityCharacteristics.h"
#include "WifiCharacteristics.h"
#include "AssociationCharacteristics.h"
#include "LampCharacteristics.h"



#define DEVICE_INFO_SERVICE_UUID  "180a"
#define MANUFACTURER_CH_UUID      "2a29"
#define MODEL_CH_UUID             "2a24"
#define SERIAL_CH_UUID            "2a25"

#define UTILITY_SERVICE_UUID      "1001A7D3-D8A4-4FEA-8174-1736E808C066"

#define WIFI_SERVICE_UUID         "3001A7D3-D8A4-4FEA-8174-1736E808C066"

#define ASSOCIATION_SERVICE_UUID  "2001A7D3-D8A4-4FEA-8174-1736E808C066"

#define LAMP_SERVICE_UUID         "0001A7D3-D8A4-4FEA-8174-1736E808C066"



/**

*/
class BLE {
  public:
    BLEServer *server;
    std::string deviceID;
    std::string deviceName;

    BLEService *deviceInfoService;
    BLECharacteristic *manufacturerCharacteristic;
    BLECharacteristic *modelCharacteristic;
    BLECharacteristic *serialCharacteristic;

    BLEService *utilityService;

    BLEService *wifiService;

    BLEService *associationService;
    AssociationCodeCharacteristic *associationCodeCharacteristic;
    IsAssociatedCharacteristic *isAssociatedCharacteristic;

    BLEService *lampService;
    HSVCharacteristic *hsvCharacteristic;
    BrightnessCharacteristic *brightnessCharacteristic;
    OnOffCharacteristic *onOffCharacteristic;

    LampState *lampState;

    BLE(LampState* lampState) {
      this->lampState = lampState;

      uint64_t efuse = ESP.getEfuseMac();
      deviceID = mac2String((byte*) &efuse);
      deviceName = "MOONLAMP-";
      deviceName += deviceID;
      Serial.println(deviceName.c_str());

      BLEDevice::init(deviceName);
      server = BLEDevice::createServer();

      setupDeviceInfoService();
      setupUtilityService();
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

    void setupUtilityService() {
      utilityService = server->createService(UTILITY_SERVICE_UUID);
    }

    void setupWifiService() {
      wifiService = server->createService(WIFI_SERVICE_UUID);
    }

    void setupAssociationService() {
      associationService = server->createService(ASSOCIATION_SERVICE_UUID);
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

    std::string mac2String(byte ar[]) {
      std::string s;
      for (byte i = 0; i < 6; ++i)
      {
        char buf[3];
        sprintf(buf, "%02X", ar[i]); // J-M-L: slight modification, added the 0 in the format for padding
        s += buf;
      }
      std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c) {
        return std::tolower(c);
      });
      return s;
    }

};
