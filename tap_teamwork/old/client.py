import requests
import singer

LOGGER = singer.get_logger()  # noqa


class Client:

    MAX_TRIES = 5

    def __init__(self, config):
        self.config = config

    def make_request(self, url, method, params=None, body=None):
        LOGGER.info("Making %s request to %s (%s)", method, url, params)

        # Basic Auth requires API Key as user with any password string
        auth = requests.auth.HTTPBasicAuth(self.config["api_key"], "xxx")
        response = requests.request(
            method,
            url,
            headers={"Content-Type": "application/json"},
            auth=auth,
            params=params,
            json=body,
        )

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()
