import json
import paho.mqtt.client as mqtt


class LampState():
    def __init__(self):
        self.is_on = True
        self.brightness = 0xFF
        self.hue = 0xFF
        self.saturation = 0xFF
        self.value = 0xFF
        self.client_id = 'lamp_bt_peripheral'
        self.has_received_first_update = False

        self.client_connection_topic = 'lamp/connection/' + self.client_id + '/state'

    def set_onoff(self, is_on):
        self.is_on = is_on

    def set_brightness(self, brightness):
        self.brightness = brightness

    def set_hsv(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value
