import paho.mqtt.client as mqtt
import json


class MQTTClient:
    MQTT_VERSION = mqtt.MQTTv311
    MQTT_BROKER_HOST = "localhost"
    MQTT_BROKER_PORT = 1883
    MQTT_BROKER_KEEP_ALIVE_SECS = 60

    client_id = 'device_bt_peripheral'

    def __init__(self):
        self.client_state_topic = f"device/connection/{self.client_id}/state"
        self.client = self._create_and_configure_broker_client()
        self.client.connect(self.MQTT_BROKER_HOST,
                            port=self.MQTT_BROKER_PORT,
                            keepalive=self.MQTT_BROKER_KEEP_ALIVE_SECS)
        self.client.loop_start()

    def _create_and_configure_broker_client(self):
        client = mqtt.Client(client_id=self.client_id, protocol=self.MQTT_VERSION)
        client.will_set(self.client_state_topic, "0", qos=2, retain=True)
        client.enable_logger()
        client.on_connect = self.on_connect
        client.on_message = self.default_on_message
        return client

    def on_connect(self, client, userdata, rc, unknown):
        self.client.publish(self.client_state_topic, "1", qos=2, retain=True)

    def default_on_message(self, client, userdata, msg):
        print("Received unexpected message on topic " +
              msg.topic + " with payload '" + str(msg.payload) + "'")

    def publish_dict(self, topic, message_dict, **kwargs):
        message_dict['client'] = self.client_id
        self.client.publish(topic, json.dumps(message_dict), **kwargs)
