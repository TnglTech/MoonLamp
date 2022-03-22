import paho.mqtt.client

TOPIC_WIFI_UPDATE = "wifi/set_config"
TOPIC_WIFI_RESPONSE = "wifi/response"
TOPIC_WIFI_CONFIG_SERVICE_STATE = "wifi/connection/wifi_config_service/state"

# MQTT Broker Connection info
MQTT_VERSION = paho.mqtt.client.MQTTv311
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_BROKER_KEEP_ALIVE_SECS = 60
