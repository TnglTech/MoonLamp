import paho.mqtt.client

DEVICE_ID_FILENAME = '/sys/class/net/wlan0/address'

# MQTT Topic Names
TOPIC_SET_LAMP_CONFIG = "lamp_service/set_config"
TOPIC_LAMP_CHANGE_NOTIFICATION = "lamp_service/changed"
TOPIC_LAMP_ASSOCIATED = "lamp_service/associated"
TOPIC_NOTIFICATION = "lamp_service/notification"


def get_device_id():
    mac_addr = open(DEVICE_ID_FILENAME).read().strip()
    return mac_addr.replace(':', '')


def client_state_topic(client_id):
    return 'device/connection/{}/state'.format(client_id)


def broker_bridge_connection_topic():
    device_id = get_device_id()
    return '$SYS/broker/connection/{}_moonlamp_broker/state'.format(device_id)


# MQTT Broker Connection info
MQTT_VERSION = paho.mqtt.client.MQTTv311
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_BROKER_KEEP_ALIVE_SECS = 60
