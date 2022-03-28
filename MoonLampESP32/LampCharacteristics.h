#define HSV_CHARACTERISTIC_UUID "0002A7D3-D8A4-4FEA-8174-1736E808C066"
#define BRIGHTNESS_CHARACTERISTIC_UUID "0003A7D3-D8A4-4FEA-8174-1736E808C066"
#define ON_OFF_CHARACTERISTIC_UUID "0004A7D3-D8A4-4FEA-8174-1736E808C066"

/**
 * 
 */
class HSVCharacteristic: public BLECharacteristic {
  public:
    HSVCharacteristic(): BLECharacteristic(BLEUUID(HSV_CHARACTERISTIC_UUID)) {
      setHSV(255, 255);
    }
  
    void setHSV(uint16_t hue, uint16_t saturation) {
      uint32_t data = hue;
      data += saturation << 8;
      setValue(data);
    }
};




/**
 * 
 */
class BrightnessCharacteristic: public BLECharacteristic {
  public:
    BrightnessCharacteristic(): BLECharacteristic(BLEUUID(BRIGHTNESS_CHARACTERISTIC_UUID)) {
      setBrightness(255);
    }
  
    void setBrightness(uint8_t brightness) {
      setValue(&brightness, 1);
    }
};




/**
 * 
 */
class OnOffCharacteristic: public BLECharacteristic {
  public:
    OnOffCharacteristic(): BLECharacteristic(BLEUUID(ON_OFF_CHARACTERISTIC_UUID)) {
      setOnOff(0);
    }
  
    void setOnOff(uint8_t is_on) {
        setValue(&is_on, 1);
    }
};
