import sys
import json

TOPIC_WIFI_PUBLISH = 'wifi/set_config'
TOPIC_WIFI_SUBSCRIBE = 'wifi/response'


class WifiState:
    def __init__(self, helper):
        self._helper = helper
        self._mqtt_client = helper.mqtt_client
        self._client = self._mqtt_client.client

        self.ssid = ""
        self.psk = ""
        self.last_attempt = False
        self.last_attempt_feedback = "TODO: IMPLEMENT FEEDBACK"
        self.has_received_first_update = False

        self.update_action_callback = None
        self.feedback_callback = None

        self._setup_mqtt_callbacks()

    def _setup_mqtt_callbacks(self):
        self._client.message_callback_add(TOPIC_WIFI_SUBSCRIBE,
                                          self.on_receive_wifi_message)
        self._client.subscribe(TOPIC_WIFI_SUBSCRIBE, qos=1)

    def on_receive_wifi_message(self, client, userdata, msg):
        new_data = json.loads(msg.payload.decode('utf-8'))
        print(new_data)

        if 'status' not in new_data:
            #TODO: throw error
            return

        if new_data['status'] is True:
            self.last_attempt = True
        else:
            self.last_attempt = False

        if self.update_action_callback is not None:
            self.update_action_callback(self.last_attempt)

        if self.feedback_callback is not None:
            self.feedback_callback(self.last_attempt_feedback)

    def set_ssid(self, ssid):
        self.ssid = ssid

    def set_psk(self, psk):
        self.psk = psk

    def join_wifi(self):
        if not self.ssid:
            print("Missing SSID")
            self.last_attempt = False
            return

        msg = {'ssid': self.ssid}
        if self.psk:
            msg['psk'] = self.psk
        self._mqtt_client.publish_dict(TOPIC_WIFI_PUBLISH, msg, qos=1)
        print("set wifi data")





