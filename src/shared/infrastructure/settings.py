from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Hexagonal Example"
    database_url: str = "sqlite:///./app.db"
    db_echo: bool = False
    # When unset, posts use in-process user lookup; when set, HTTP + internal_api_key.
    users_service_url: str | None = None
    # When unset, users use in-process post access; when set, HTTP + internal_api_key.
    posts_service_url: str | None = None
    # Service-to-service: same value on every service that exposes or calls /internal/*.
    # In production, pair with private network / ingress policies (not public internet).
    internal_api_key: str | None = None
    internal_api_header_name: str = "X-Internal-Token"

    @field_validator("users_service_url", "posts_service_url", mode="before")
    @classmethod
    def _empty_url_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
