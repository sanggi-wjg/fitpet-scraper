import os
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
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


@lru_cache
def get_settings() -> Settings:
    settings = Settings()  # type: ignore[call-arg]
    for path in [settings.directory.log, settings.directory.data]:
        os.makedirs(path, exist_ok=True)
    return settings
