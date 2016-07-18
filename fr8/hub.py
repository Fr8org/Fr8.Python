import json
import urllib2

import data


def create_default_hub(hub_url, terminal_id, terminal_secret, container_id, user_id):
    return Hub(hub_url, terminal_id, terminal_secret, container_id, user_id)


class Hub(object):
    def __init__(self, hub_url, terminal_id, terminal_secret, container_id, user_id):
        self.hub_url = hub_url
        self.terminal_id = terminal_id
        self.terminal_secret = terminal_secret
        self.container_id = container_id
        self.user_id = user_id

    def get_payload(self):
        payload_url = self.hub_url + 'api/v1/containers/payload?id=' + self.container_id
        auth_header = Hub.generate_authentication_header(
            self.terminal_secret,
            self.user_id
        )

        headers = {
            "Authorization": "FR8-TOKEN " + auth_header
        }
        request = urllib2.Request(payload_url, headers=headers)
        contents = urllib2.urlopen(request).read()
        return data.PayloadDTO.from_fr8_json(json.loads(contents))

    @staticmethod
    def generate_authentication_header(terminal_secret, user_id):
        result = 'key=' + terminal_secret
        if user_id:
            result += ', user=' + user_id

        return result
