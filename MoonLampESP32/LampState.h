class LampState {
  

  public:
    uint8_t hue = 255;
    uint8_t saturation = 255;
    uint8_t brightness = 255;
    bool is_on = true;
    
    LampState() {
    }

    void setHue(uint8_t hue) {
      this->hue = hue;
    }

    void setSaturation(uint8_t saturation) {
      this->saturation = saturation;
    }

    void setBrightness(uint8_t brightness) {
      this->brightness = brightness;
    }

    void setIsOn(bool is_on) {
      this->is_on = is_on;
    }
};
