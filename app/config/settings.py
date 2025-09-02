import json
import os
from functools import lru_cache
from typing import Any

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSSecretsManager:

    def __init__(self, region_name: str = "ap-northeast-2"):
        self.client = boto3.client("secretsmanager", region_name=region_name)

    def get_secret(self) -> dict[str, Any]:
        try:
            response = self.client.get_secret_value(SecretId="fitpet-scraper")
            secret_string = response.get("SecretString")
            if secret_string:
                return json.loads(secret_string)
            return {}
        except (ClientError, BotoCoreError, json.JSONDecodeError) as e:
            raise RuntimeError(f"😢😢😢 AWS Secrets Manager 비밀 값을 가져오는데 실패했습니다: {e}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env" if os.getenv("ENVIRONMENT", "local") == "local" else None,
        env_file_encoding="UTF-8",
        env_nested_delimiter="__",
        nested_model_default_partial_update=False,
    )

    class NaverShoppingValue(BaseModel):
        client_id: str
        client_secret: str

    class SqliteDatabaseValue(BaseModel):
        path: str

    class CeleryValue(BaseModel):
        broker: str
        backend: str
        once_backend: str
        once_default_timeout: int  # seconds

    class SlackValue(BaseModel):
        bot_token: str
        channel_fitpet_scraper_id: str

    class DirectoryValue(BaseModel):
        base: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        @property
        def log(self):
            return os.path.join(self.base, "logs")

        @property
        def data(self):
            return os.path.join(self.base, "data")

    naver_shopping: NaverShoppingValue
    sqlite_database: SqliteDatabaseValue
    celery: CeleryValue
    slack: SlackValue
    directory: DirectoryValue = DirectoryValue()

    def __init__(self, **kwargs):
        if os.getenv("ENVIRONMENT", "local") != "local":
            aws_secrets_manager = AWSSecretsManager()
            secrets = aws_secrets_manager.get_secret()

            for key, value in secrets.items():
                os.environ[key.upper()] = str(value)

        super().__init__(**kwargs)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()  # type: ignore[call-arg]
    for path in [settings.directory.log, settings.directory.data]:
        os.makedirs(path, exist_ok=True)
    return settings
