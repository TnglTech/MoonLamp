#!/usr/bin/env python3

import json
import paho.mqtt.client as mqtt
import shelve
import colorsys
import time
from rpi_ws281x import Color, PixelStrip, ws

from lamp_common import *

LAMP_STATE_FILENAME = "lamp_state"
MQTT_CLIENT_ID = "lamp_service"

FP_DIGITS = 2
FLASH_DELAY = 0.3

# LED Strip Config
LED_COUNT = 30
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

class InvalidLampConfig(Exception):
    pass

class InvalidNotificationStructure(Exception):
    pass

class LampDriver(object):
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def change_color(self, *args):
        color = Color(args[0], args[1], args[2])
        for i in range(0, self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()


class LampService(object):
    def __init__(self):
        self.lamp_driver = LampDriver()
        self._client = self._create_and_configure_broker_client()
        self.db = shelve.open(LAMP_STATE_FILENAME, writeback=True)
        if 'color' not in self.db:
            self.db['color'] = {'h': round(1.0, FP_DIGITS),
                                's': round(1.0, FP_DIGITS)}
        if 'brightness' not in self.db:
            self.db['brightness'] = round(1.0, FP_DIGITS)
        if 'on' not in self.db:
            self.db['on'] = False
        if 'client' not in self.db:
            self.db['client'] = ''
        self.write_current_settings_to_hardware()

    def _create_and_configure_broker_client(self):
        client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=MQTT_VERSION)
        client.will_set(client_state_topic(MQTT_CLIENT_ID), "0",
                        qos=2, retain=True)
        client.enable_logger()
        client.on_connect = self.on_connect
        client.message_callback_add(TOPIC_SET_LAMP_CONFIG,
                                    self.on_message_set_config)
        client.message_callback_add(TOPIC_NOTIFICATION,
                                    self.on_notification)
        client.on_message = self.default_on_message
        return client

    def serve(self):
        self._client.connect(MQTT_BROKER_HOST,
                             port=MQTT_BROKER_PORT,
                             keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        self._client.loop_forever()

    def on_connect(self, client, userdata, rc, unknown):
        self._client.publish(client_state_topic(MQTT_CLIENT_ID), "1",
                             qos=2, retain=True)
        self._client.subscribe(TOPIC_SET_LAMP_CONFIG, qos=1)
        self._client.subscribe(TOPIC_NOTIFICATION, qos=2)
        # publish current lamp state at startup
        self.publish_config_change()

    def default_on_message(self, client, userdata, msg):
        print("Received unexpected message on topic " +
              msg.topic + " with payload '" + str(msg.payload) + "'")

    def on_message_set_config(self, client, userdata, msg):
        try:
            new_config = json.loads(msg.payload.decode('utf-8'))
            if 'client' not in new_config:
                raise InvalidLampConfig()
            self.set_last_client(new_config['client'])
            if 'on' in new_config:
                self.set_current_onoff(new_config['on'])
            if 'color' in new_config:
                self.set_current_color(new_config['color'])
            if 'brightness' in new_config:
                self.set_current_brightness(new_config['brightness'])
            self.publish_config_change()
        except InvalidLampConfig:
            print("error applying new settings " + str(msg.payload))

    def on_notification(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode('utf-8'))
        try:
            if 'type' not in payload:
                raise InvalidNotificationStructure()

            if payload['type'] == 'doorbell_event':
                self.handle_doorbell_event(payload)
            else:
                raise InvalidNotificationStructure()

        except InvalidNotificationStructure:
            print("Error reading notification")

    def publish_config_change(self):
        config = {'color': self.get_current_color(),
                  'brightness': self.get_current_brightness(),
                  'on': self.get_current_onoff(),
                  'client': self.get_last_client()}
        self._client.publish(TOPIC_LAMP_CHANGE_NOTIFICATION,
                             json.dumps(config).encode('utf-8'), qos=1,
                             retain=True)

    def get_last_client(self):
        return self.db['client']

    def set_last_client(self, new_client):
        self.db['client'] = new_client

    def get_current_brightness(self):
        return self.db['brightness']

    def set_current_brightness(self, new_brightness):
        if new_brightness < 0 or new_brightness > 1.0:
            raise InvalidLampConfig()
        self.db['brightness'] = round(new_brightness, FP_DIGITS)
        self.write_current_settings_to_hardware()

    def get_current_onoff(self):
        return self.db['on']

    def set_current_onoff(self, new_onoff):
        if new_onoff not in [True, False]:
            raise InvalidLampConfig()
        self.db['on'] = new_onoff
        self.write_current_settings_to_hardware()

    def get_current_color(self):
        return self.db['color'].copy()

    def set_current_color(self, new_color):
        for ch in ['h', 's']:
            if new_color[ch] < 0 or new_color[ch] > 1.0:
                raise InvalidLampConfig()
        for ch in ['h', 's']:
            self.db['color'][ch] = round(new_color[ch], FP_DIGITS)
        self.write_current_settings_to_hardware()

    def write_current_settings_to_hardware(self):
        onoff = self.get_current_onoff()
        brightness = self.get_current_brightness()
        color = self.get_current_color()

        r, g, b = self.calculate_rgb(color['h'], color['s'], brightness, onoff)
        self.lamp_driver.change_color(r, g, b)
        self.db.sync()

    def calculate_rgb(self, hue, saturation, brightness, is_on):
        pwm = float(LED_BRIGHTNESS)
        r, g, b = 0.0, 0.0, 0.0

        if is_on:
            rgb = colorsys.hsv_to_rgb(hue, saturation, 1.0)
            r, g, b = tuple(channel * pwm * brightness
                            for channel in rgb)
        return r, g, b

    def handle_doorbell_event(self, message):
        try:
            hue = 1.0
            saturation = 1.0
            brightness = 1.0
            num_flashes = 5
            if 'hue' in message:
                hue = self.convert_to_lamp_values(message['hue'])
            if 'saturation' in message:
                saturation = self.convert_to_lamp_values(message['saturation'])
            if 'brightness' in message:
                brightness = self.convert_to_lamp_values(message['brightness'])
            if 'num_flashes' in message:
                num_flashes = message['num_flashes']
            self.do_flashing(hue, saturation, brightness, num_flashes)
        except InvalidNotificationStructure:
            print("Error reading notification")

    def convert_to_lamp_values(self, value):
        if value < 0 or value > 1.0:
            raise InvalidLampConfig()
        return round(value, FP_DIGITS)

    def do_flashing(self, hue, saturation, brightness, num_flashes):
        r, g, b = self.calculate_rgb(hue, saturation, brightness, True)
        for _ in range(0, num_flashes):
            print("Thing")
            self.lamp_driver.change_color(r, g, b)
            time.sleep(FLASH_DELAY)
            self.lamp_driver.change_color(0, 0, 0)
            time.sleep(FLASH_DELAY)
        self.write_current_settings_to_hardware()


if __name__ == '__main__':
    lamp = LampService().serve()