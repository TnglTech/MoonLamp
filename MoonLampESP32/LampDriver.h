#include <Adafruit_NeoPixel.h>

#define LED_PIN 6
#define LED_COUNT 69

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_RGB + NEO_KHZ800);

class LampDriver {
  private:
    LampState *lampState;

  public:
    LampDriver(LampState* lampState) {
      this->lampState = lampState;

      strip.begin();
      strip.show();
    }
};
