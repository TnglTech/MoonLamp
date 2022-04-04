from mqtt_client import MQTTClient
import shelve

DEVICE_ID_FILENAME = '/sys/class/net/wlan0/address'
DB_FILENAME = "utility"


class Helper:
    def __init__(self):
        self.mqtt_client = MQTTClient()
        self.db = shelve.open(DB_FILENAME, writeback=True)

    @staticmethod
    def get_device_id():
        mac_addr = open(DEVICE_ID_FILENAME).read().strip()
        return mac_addr.replace(':', '')
