import json

TOPIC_DEVICE_ASSOCIATED = "device/associated"


class AssociationState:
    def __init__(self, helper):
        self._helper = helper

        self._db = helper.db
        self._initialize_db()

        self._mqtt_client = helper.mqtt_client
        self._client = self._mqtt_client.client

        self.association_code_callback = None

        self._setup_mqtt_callbacks()

    def _initialize_db(self):
        if self._db is None:
            raise Exception("DB is not open")

        if 'association' not in self._db:
            self._db['association'] = {}
            self._db['association']['is_associated'] = False
            self._db['association']['association_code'] = ""

    def _setup_mqtt_callbacks(self):
        self._client.message_callback_add(TOPIC_DEVICE_ASSOCIATED,
                                          self.on_receive_message)
        self._client.subscribe(TOPIC_DEVICE_ASSOCIATED, qos=2)

    def on_receive_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode('utf-8'))
        if 'associated' in data:
            self.is_associated = data['associated']
        if 'code' in data:
            self.association_code = data['code']

    def get_association_code(self):
        if not self.is_associated:
            return self._db['association']['association_code']
        return ""

    def set_association_code(self, val):
        self._db['association']['association_code'] = val

    association_code = property(get_association_code, set_association_code)

    def get_is_associated(self):
        return self._db['association']['is_associated']

    def set_is_associated(self, val):
        self._db['association']['is_associated'] = val

    is_associated = property(get_is_associated, set_is_associated)
