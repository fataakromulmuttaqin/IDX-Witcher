from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://iw:iw@localhost:5432/idxwitcher"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:5173"]
    timezone: str = "Asia/Jakarta"
    pipeline_hour: int = 17
    yahoo_batch_size: int = 50
    yahoo_batch_sleep: float = 1.5
    alert_webhook_url: str | None = None
    history_start: str = "2021-01-01"


@lru_cache
def get_settings() -> Settings:
    return Settings()
