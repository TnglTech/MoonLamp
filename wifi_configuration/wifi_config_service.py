#!/usr/bin/env python3
from wifi_common import *
from wifi_configurator import WifiConfigurator
import paho.mqtt.client as mqtt
import json

MQTT_CLIENT_ID = "wifi_config_service"


class InvalidWifiConfig(Exception):
    pass


class WifiConfigService(object):
    def __init__(self):
        self.lastClient = ""
        self._client = self._create_and_configure_broker_client()

    def _create_and_configure_broker_client(self):
        client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=MQTT_VERSION)
        client.will_set(TOPIC_WIFI_CONFIG_SERVICE_STATE, "0", qos=2, retain=True)
        client.enable_logger()
        client.on_connect = self.on_connect
        client.message_callback_add(TOPIC_WIFI_UPDATE, self.on_message_set_config)
        client.on_message = self.default_on_message
        return client

    def serve(self):
        self._client.connect(MQTT_BROKER_HOST,
                             port=MQTT_BROKER_PORT,
                             keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        self._client.loop_forever()

    def on_connect(self, client, userdata, rc, unknown):
        self._client.publish(TOPIC_WIFI_CONFIG_SERVICE_STATE, "1",
                             qos=2, retain=True)
        self._client.subscribe(TOPIC_WIFI_UPDATE, qos=2)

    def default_on_message(self, client, userdata, msg):
        print("Received unexpected message on topic " +
              msg.topic + " with payload '" + str(msg.payload) + "'")

    def on_message_set_config(self, client, userdata, msg):
        _ssid = None
        _psk = None
        try:
            new_config = json.loads(msg.payload.decode('utf-8'))
            if 'client' not in new_config:
                raise InvalidWifiConfig()
            self.lastClient = new_config['client']
            if 'ssid' in new_config:
                _ssid = new_config['ssid']
            else:
                raise InvalidWifiConfig("SSID is missing.")
            if 'psk' in new_config:
                _psk = new_config['psk']

            result, msg = WifiConfigurator(_ssid, _psk).reconfigure()
            if result:
                print("updated wifi_service")
                self.publish_config_change(True, message=msg)
            else:
                self.publish_config_change(False, message=msg)
                #raise InvalidWifiConfig()
        except InvalidWifiConfig as ex:
            self.publish_config_change(False, message=(ex.message or "Invalid WiFi configuration data."))
            print("Error applying new wifi_service settings " + str(msg.payload))

    def publish_config_change(self, status, message=""):
        config = {'client': self.lastClient,
                  'status': status}
        if message != "":
            config['message'] = message

        self._client.publish(TOPIC_WIFI_RESPONSE,
                             json.dumps(config).encode('utf-8'), qos=2)


if __name__ == '__main__':
    config_service = WifiConfigService().serve()
