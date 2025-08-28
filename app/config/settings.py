from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../../.env",),
        env_file_encoding="UTF-8",
        env_nested_delimiter="__",
        nested_model_default_partial_update=True,
    )

    class SqliteDatabase(BaseModel):
        path: str = "sqlite:///master.db"

    class NaverShopping(BaseModel):
        client_id: str
        client_secret: str

    class Celery(BaseModel):
        broker = "redis://localhost:6379/0"
        backend = "sqlite:///master.db"
        once_backend = "redis://localhost:6379/1"
        once_default_timeout = 60 * 60  # 1시간

    sqlite_database: SqliteDatabase
    naver_shopping: NaverShopping
    celery: Celery


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
