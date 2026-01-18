"""Configuration management with Pydantic Settings v2."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with Pydantic validation.

    All settings are loaded from environment variables with validation.
    Use .env file for local development.
    """

    # App settings
    app_name: str = "Telemetriya"
    version: str = "0.1.0"
    debug: bool = False

    # Telegram settings
    telegram_token: str = Field(..., validation_alias="TELEGRAM_TOKEN")
    telegram_webhook_url: Optional[str] = Field(None, validation_alias="TELEGRAM_WEBHOOK_URL")

    # Database settings
    db_url: str = Field(..., validation_alias="DATABASE_URL")

    # LLM settings
    llm_provider: str = Field(default="ollama", validation_alias="LLM_PROVIDER")
    llm_api_key: Optional[str] = Field(None, validation_alias="LLM_API_KEY")
    llm_base_url: Optional[str] = Field(None, validation_alias="LLM_BASE_URL")
    llm_model: Optional[str] = Field(None, validation_alias="LLM_MODEL")

    # Todoist settings
    todoist_api_key: Optional[str] = Field(None, validation_alias="TODOIST_API_KEY")

    # Storage settings
    storage_path: str = Field(default="./storage", validation_alias="STORAGE_PATH")

    # Security settings
    secret_key: str = Field(..., validation_alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # Logging settings
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_format: str = Field(default="json", validation_alias="LOG_FORMAT")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Get cached Settings instance (singleton).

    Pydantic Settings reads configuration from environment variables
    or .env file. The @lru_cache decorator ensures we only create
    one instance during the application lifecycle.

    Returns:
        Settings: Cached application settings instance.
    """
    return Settings()  # type: ignore[call-arg]
