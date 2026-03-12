import logging
import os
import ssl

import certifi
from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class SlackClient:
    """
    https://github.com/slackapi/python-slack-sdk
    """

    def __init__(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(token=settings.slack.bot_token, ssl=ssl_context)

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(2),
        retry=retry_if_exception_type((SlackClientError,)),
    )
    def upload_file(self, filepath: str, channel: str) -> bool:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        self.client.files_upload_v2(file=filepath, channel=channel)
        return True

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(2),
        retry=retry_if_exception_type((SlackClientError,)),
    )
    def post_message(self, channel: str, text: str) -> bool:
        self.client.chat_postMessage(channel=channel, text=text)
        return True
