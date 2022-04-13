import sys
import json

sys.path.append("../bluetooth")

# MQTT Topic Names
TOPIC_SET_LAMP_CONFIG = "lamp_service/set_config"
TOPIC_LAMP_CHANGE_NOTIFICATION = "lamp_service/changed"
TOPIC_NOTIFICATION = "lamp_service/notification"


class RGBLampState():
    def __init__(self, helper):
        self._helper = helper
        self._mqtt_client = helper.mqtt_client
        self._client = self._mqtt_client.client

        self.is_on = True
        self.brightness = 0xFF
        self.hue = 0xFF
        self.saturation = 0xFF
        self.value = 0xFF
        self.has_received_first_update = False

        self.onoff_update_callback = None
        self.brightness_update_callback = None
        self.hsv_update_callback = None

        self._setup_mqtt_callbacks()

    def _setup_mqtt_callbacks(self):
        self._client.message_callback_add(TOPIC_LAMP_CHANGE_NOTIFICATION,
                                          self.on_receive_change)
        self._client.subscribe(TOPIC_LAMP_CHANGE_NOTIFICATION, qos=1)

    def set_onoff(self, is_on):
        self.is_on = is_on
        msg = {'on': self.is_on}
        self._mqtt_client.publish_dict(TOPIC_SET_LAMP_CONFIG, msg, qos=1)

    def set_brightness(self, brightness):
        self.brightness = brightness
        msg = {'brightness': self.brightness / 0xFF}
        self._mqtt_client.publish_dict(TOPIC_SET_LAMP_CONFIG, msg, qos=1)

    def set_hsv(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value
        msg = {'color': {'h': self.hue / 0xFF, 's': self.saturation / 0xFF}}
        self._mqtt_client.publish_dict(TOPIC_SET_LAMP_CONFIG, msg, qos=1)

    def on_receive_change(self, client, userdata, msg):
        new_state = json.loads(msg.payload.decode('utf-8'))

        if new_state['client'] == self._mqtt_client.client_id and self.has_received_first_update:
            return

        new_onoff = new_state['on']
        new_brightness = round(new_state['brightness'] * 0xFF)
        new_hue = round(new_state['color']['h'] * 0xFF)
        new_saturation = round(new_state['color']['s'] * 0xFF)

        print(new_state)

        if self.is_on != new_onoff:
            self.is_on = new_onoff
            if self.onoff_update_callback is not None:
                self.onoff_update_callback(self.is_on)

        if self.brightness != new_brightness:
            self.brightness = new_brightness
            if self.brightness_update_callback is not None:
                self.brightness_update_callback(self.brightness)

        if self.hue != new_hue or self.saturation != new_saturation:
            self.hue = new_hue
            self.saturation = new_saturation
            if self.hsv_update_callback is not None:
                self.hsv_update_callback(self.hue, self.saturation, self.value)

        self.has_received_first_update = True
