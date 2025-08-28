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
        once_default_timeout: int

    naver_shopping: NaverShoppingValue
    sqlite_database: SqliteDatabaseValue
    celery: CeleryValue


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
