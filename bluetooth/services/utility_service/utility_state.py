class UtilityState:
    def __init__(self, helper):
        self._helper = helper

        self._db = helper.db
        self._initialize_db()

        self._mqtt_client = helper.mqtt_client
        self._client = self._mqtt_client.client

        self._device_name = ""

    def _initialize_db(self):
        if self._db is None:
            raise Exception("DB is not open")

        if 'device_name' not in self._db:
            self._db['device_name'] = "MoonLamp - " + self._helper.get_device_id()

    def get_device_name(self):
        return self._db['device_name']

    def set_device_name(self, val):
        self._db['device_name'] = val

    device_name = property(get_device_name, set_device_name)
