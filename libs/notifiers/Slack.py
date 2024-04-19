import requests

from libs.config import SLACK_TOKEN, SLACK_CHANNEL
from libs.notifiers.Notifier import Notifier


class Slack(Notifier):
    enabled_env_name = "SLACK_ENABLED"

    def send_message(self, message: str):
        url = "https://slack.com/api/chat.postMessage"

        request_data = {
            "token": SLACK_TOKEN,
            "channel": SLACK_CHANNEL,
            "text": message,
        }

        response = requests.post(
            url=url,
            data=request_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            raise ValueError(data)
