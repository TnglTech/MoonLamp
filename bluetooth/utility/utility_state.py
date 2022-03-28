class UtilityState:
    def __init__(self, helper):
        self._helper = helper
        self._mqtt_client = helper.mqtt_client
        self._client = self._mqtt_client.client
