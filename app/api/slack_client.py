import logging
import os
import ssl

import certifi
from slack_sdk import WebClient

from app.config.settings import get_settings
from app.util.decorators import run_catching

logger = logging.getLogger(__name__)
settings = get_settings()


class SlackClient:
    """
    https://github.com/slackapi/python-slack-sdk
    """

    def __init__(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(token=settings.slack.bot_token, ssl=ssl_context)

    @run_catching
    def upload_file(self, filepath: str, channel: str) -> bool:
        if not os.path.exists(filepath):
            raise Exception(f"File not found: {filepath}")

        self.client.files_upload_v2(file=filepath, channel=channel)
        return True

    @run_catching
    def post_message(self, channel: str, text: str) -> bool:
        self.client.chat_postMessage(channel=channel, text=text)
        return True
