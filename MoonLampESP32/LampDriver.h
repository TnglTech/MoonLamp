//#include <Adafruit_NeoPixel.h>
//
//#define LED_PIN 21
//#define LED_COUNT 2
//
//Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_RGB + NEO_KHZ800);
//
//class LampDriver {
//  private:
//    LampState *lampState;
//
//  public:
//    LampDriver(LampState* lampState) {
//      this->lampState = lampState;
//
//      strip.begin();
//      strip.show();
//    }
//};
//#define FASTLED_RMT_MAX_CHANNELS 1
//#define FASTLED_RMT_BUILTIN_DRIVER 1
#define FASTLED_ALLOW_INTERRUPTS 0
#define LED_TYPE WS2812
#include "FastLED.h"
#define NUM_LEDS 3
CRGB leds[NUM_LEDS];

class LampDriver {
  private:
    LampState *lampState;

  public:
    LampDriver(LampState* lampState) {
      this->lampState = lampState;

      FastLED.addLeds<WS2812, 21>(leds, NUM_LEDS);

      leds[0] = CRGB::White;
      leds[1] = CRGB::White;

      FastLED.show();
      delay(10);
      FastLED.show();

//      strip.begin();
//      strip.show();
    }
};
