import json
import paho.mqtt.client as mqtt

# MQTT Topic Names
TOPIC_SET_LAMP_CONFIG = "lamp/set_config"
TOPIC_LAMP_CHANGE_NOTIFICATION = "lamp/changed"
TOPIC_LAMP_ASSOCIATED = "lamp/associated"
TOPIC_NOTIFICATION = "lamp/notification"

MQTT_VERSION = mqtt.MQTTv311
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_BROKER_KEEP_ALIVE_SECS = 60

MQTT_CLIENT_ID = 'lamp_bt_peripheral'


class LampState():
    def __init__(self):
        self.is_on = True
        self.brightness = 0xFF
        self.hue = 0xFF
        self.saturation = 0xFF
        self.value = 0xFF
        self.has_received_first_update = False

        self.onoff_update_callback = None
        self.brightness_update_callback = None
        self.hsv_update_callback = None

        self.client_state_topic = f"lamp/connection/{MQTT_CLIENT_ID}/state"
        self._client = self._create_and_configure_broker_client()
        self._client.connect(MQTT_BROKER_HOST,
                             port=MQTT_BROKER_PORT,
                             keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        self._client.loop_start()

    def set_onoff(self, is_on):
        self.is_on = is_on
        msg = {'client': MQTT_CLIENT_ID, 'on': self.is_on}
        self._client.publish(TOPIC_SET_LAMP_CONFIG, json.dumps(msg), qos=1)

    def set_brightness(self, brightness):
        self.brightness = brightness
        msg = {'client': MQTT_CLIENT_ID, 'brightness': self.brightness / 0xFF}
        self._client.publish(TOPIC_SET_LAMP_CONFIG, json.dumps(msg), qos=1)

    def set_hsv(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value
        msg = {'client': MQTT_CLIENT_ID, 'color': {'h': self.hue / 0xFF, 's': self.saturation / 0xFF}}
        self._client.publish(TOPIC_SET_LAMP_CONFIG, json.dumps(msg), qos=1)

    def _create_and_configure_broker_client(self):
        client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=MQTT_VERSION)
        client.will_set(self.client_state_topic, "0", qos=2, retain=True)
        client.enable_logger()
        client.on_connect = self.on_connect
        client.message_callback_add(TOPIC_LAMP_CHANGE_NOTIFICATION,
                                    self.on_receive_change)
        client.on_message = self.default_on_message
        return client

    def on_connect(self, client, userdata, rc, unknown):
        self._client.publish(self.client_state_topic, "1", qos=2, retain=True)
        self._client.subscribe(TOPIC_LAMP_CHANGE_NOTIFICATION, qos=1)

    def default_on_message(self, client, userdata, msg):
        print("Received unexpected message on topic " +
              msg.topic + " with payload '" + str(msg.payload) + "'")

    def on_receive_change(self, client, userdata, msg):
        new_state = json.loads(msg.payload.decode('utf-8'))

        if new_state['client'] == MQTT_CLIENT_ID and self.has_received_first_update:
            print("ignoring lamp changed update that we initiated")
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




