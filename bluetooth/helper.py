from mqtt_client import MQTTClient

DEVICE_ID_FILENAME = '/sys/class/net/wlan0/address'


class Helper:
    def __init__(self):
        self.mqtt_client = MQTTClient()

    @staticmethod
    def get_device_id():
        mac_addr = open(DEVICE_ID_FILENAME).read().strip()
        return mac_addr.replace(':', '')
