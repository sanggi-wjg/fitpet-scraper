import json
import os
from functools import lru_cache
from typing import Any, Literal
from urllib.parse import quote_plus

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, BotoCoreError
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSSecretsManager:

    def __init__(self):
        self.client = boto3.client(
            "secretsmanager",
            region_name="ap-northeast-2",
            config=Config(
                retries={"max_attempts": 3, "mode": "standard"},
                read_timeout=10,
                connect_timeout=10,
            ),
        )

    def get_secret(self) -> dict[str, Any]:
        try:
            response = self.client.get_secret_value(SecretId="fitpet-scraper")
            secret_string = response.get("SecretString")
            if secret_string:
                return json.loads(secret_string)
            return {}
        except (ClientError, BotoCoreError, json.JSONDecodeError) as e:
            raise RuntimeError(f"😢😢😢 AWS Secrets Manager 비밀 값을 가져오는데 실패했습니다: {e}")
        except Exception as e:
            raise RuntimeError(f"🔥🔥🔥 AWS Secrets Manager 비밀 값을 가져오는데 실패했습니다: {e}")


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

    class MySQLDatabaseValue(BaseModel):
        host: str
        port: int
        database: str
        user: str
        password: str
        pool_size: int = 5
        max_overflow: int = 10
        pool_timeout: int = 60
        pool_recycle: int = 1800
        pool_pre_ping: bool = True
        isolation_level: Literal["REPEATABLE READ"] | str = "REPEATABLE READ"

        @property
        def dsn(self):
            encoded_password = quote_plus(self.password)
            return f"mysql+pymysql://{self.user}:{encoded_password}@{self.host}:{self.port}/{self.database}"

    class SlackValue(BaseModel):
        bot_token: str
        channel_fitpet_scraper_id: str

    class DirectoryValue(BaseModel):
        base: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        @property
        def data(self):
            return os.path.join(self.base, "data")

    debug: bool
    naver_shopping: NaverShoppingValue
    database: MySQLDatabaseValue
    slack: SlackValue
    directory: DirectoryValue = DirectoryValue()

    def __init__(self, **kwargs):
        environment = os.getenv("ENVIRONMENT", "local")

        if environment != "local":
            aws_secrets_manager = AWSSecretsManager()
            secrets = aws_secrets_manager.get_secret()

            for key, value in secrets.items():
                os.environ[key.upper()] = str(value)

        super().__init__(**kwargs)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()  # type: ignore[call-arg]
    for path in [settings.directory.data]:
        os.makedirs(path, exist_ok=True)
    return settings
