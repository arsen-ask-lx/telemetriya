"""Unit tests for configuration management."""

import os
from pathlib import Path
from unittest.mock import patch
from typing import Generator

import pytest
from pydantic import ValidationError

# Set test environment variables before importing config
os.environ.update(
    {
        "TELEGRAM_TOKEN": "test_token_123",
        "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
        "SECRET_KEY": "test_secret_key_for_testing_purposes_only_min_16",
    }
)


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Generator[None, None, None]:
    """Clear Settings cache between tests to ensure fresh imports."""
    # Import here to avoid caching issues
    from src.core.config import get_settings, Settings

    # Clear cache before and after each test
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def isolate_from_env_file() -> Generator[None, None, None]:
    """Isolate tests from local .env file by temporarily renaming it."""
    env_file = Path(".env")
    env_backup = Path(".env.backup")

    # Rename .env to .env.backup if it exists
    if env_file.exists():
        env_file.rename(env_backup)

    try:
        yield
    finally:
        # Restore .env from .env.backup if backup exists
        if env_backup.exists():
            env_backup.rename(env_file)


@pytest.fixture
def test_env_vars() -> dict:
    """Provide test environment variables."""
    return {
        "TELEGRAM_TOKEN": "test_token_123",
        "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
        "SECRET_KEY": "test_secret_key_for_testing_purposes_only_min_16",
        "APP_NAME": "TestApp",
        "VERSION": "1.0.0",
        "DEBUG": "True",
        "LLM_PROVIDER": "test_provider",
        "STORAGE_PATH": "/test/storage",
        "LOG_LEVEL": "DEBUG",
        "LOG_FORMAT": "text",
    }


def test_settings_initialization(test_env_vars: dict) -> None:
    """Test that Settings can be initialized with all required fields."""
    from src.core.config import Settings

    with patch.dict(os.environ, test_env_vars, clear=True):
        settings = Settings()

        assert settings.app_name == "TestApp"
        assert settings.version == "1.0.0"
        assert settings.debug is True
        assert settings.telegram_token == "test_token_123"
        assert settings.db_url == "postgresql+asyncpg://test:test@localhost:5432/test_db"
        assert settings.llm_provider == "test_provider"
        assert settings.storage_path == "/test/storage"
        assert settings.secret_key == "test_secret_key_for_testing_purposes_only_min_16"
        assert settings.log_level == "DEBUG"
        assert settings.log_format == "text"


def test_settings_validation_required_fields() -> None:
    """Test that Settings raises ValidationError for missing required fields."""
    from src.core.config import Settings

    # Clear all required environment variables
    required_fields = ["TELEGRAM_TOKEN", "DATABASE_URL", "SECRET_KEY"]
    for field in required_fields:
        if field in os.environ:
            del os.environ[field]

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    errors = exc_info.value.errors()
    # Pydantic v2 returns env variable name in validation errors
    error_fields = {error["loc"][0] for error in errors}
    assert "TELEGRAM_TOKEN" in error_fields
    assert "DATABASE_URL" in error_fields
    assert "SECRET_KEY" in error_fields


def test_settings_default_values() -> None:
    """Test that Settings uses correct default values for optional fields."""
    from src.core.config import Settings

    with patch.dict(
        os.environ,
        {
            "TELEGRAM_TOKEN": "test_token",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
            "SECRET_KEY": "test_secret_16_chars",
        },
        clear=True,
    ):
        settings = Settings()

        assert settings.app_name == "Telemetriya"
        assert settings.version == "0.1.0"
        assert settings.debug is False
        assert settings.llm_provider == "ollama"
        assert settings.storage_path == "./storage"
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30
        assert settings.log_level == "INFO"
        assert settings.log_format == "json"


def test_settings_environment_variables() -> None:
    """Test that Settings correctly reads from environment variables."""
    from src.core.config import Settings

    with patch.dict(
        os.environ,
        {
            "TELEGRAM_TOKEN": "env_token",
            "DATABASE_URL": "postgresql+asyncpg://env:env@localhost:5432/env_db",
            "SECRET_KEY": "env_secret_16_chars",
            "APP_NAME": "EnvApp",
            "VERSION": "2.0.0",
            "DEBUG": "True",
            "LLM_PROVIDER": "env_provider",
            "LLM_API_KEY": "env_api_key",
            "LLM_BASE_URL": "http://env-base-url:11434",
            "LLM_MODEL": "env_model",
            "TODOIST_API_KEY": "env_todoist_key",
            "STORAGE_PATH": "/env/storage",
            "ALGORITHM": "RS256",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "60",
            "LOG_LEVEL": "WARNING",
            "LOG_FORMAT": "text",
        },
        clear=True,
    ):
        settings = Settings()

        assert settings.app_name == "EnvApp"
        assert settings.version == "2.0.0"
        assert settings.debug is True
        assert settings.telegram_token == "env_token"
        assert settings.db_url == "postgresql+asyncpg://env:env@localhost:5432/env_db"
        assert settings.llm_provider == "env_provider"
        assert settings.llm_api_key == "env_api_key"
        assert settings.llm_base_url == "http://env-base-url:11434"
        assert settings.llm_model == "env_model"
        assert settings.todoist_api_key == "env_todoist_key"
        assert settings.storage_path == "/env/storage"
        assert settings.algorithm == "RS256"
        assert settings.access_token_expire_minutes == 60
        assert settings.log_level == "WARNING"
        assert settings.log_format == "text"


def test_settings_caching() -> None:
    """Test that get_settings() returns cached singleton instance."""
    from src.core.config import get_settings

    # Ensure required env vars are set
    with patch.dict(
        os.environ,
        {
            "TELEGRAM_TOKEN": "test_token",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
            "SECRET_KEY": "test_secret_16_chars",
        },
        clear=True,
    ):
        settings1 = get_settings()
        settings2 = get_settings()

        # Should be the same object due to @lru_cache
        assert settings1 is settings2


def test_settings_optional_fields_none() -> None:
    """Test that optional fields can be None."""
    from src.core.config import Settings

    with patch.dict(
        os.environ,
        {
            "TELEGRAM_TOKEN": "test_token",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
            "SECRET_KEY": "test_secret_16_chars",
        },
        clear=True,
    ):
        settings = Settings()

        # Optional fields should be None when not provided
        assert settings.telegram_webhook_url is None
        assert settings.llm_api_key is None
        assert settings.llm_base_url is None
        assert settings.llm_model is None
        assert settings.todoist_api_key is None


def test_settings_model_config_extra_ignore() -> None:
    """Test that Settings ignores extra environment variables."""
    from src.core.config import Settings

    with patch.dict(
        os.environ,
        {
            "TELEGRAM_TOKEN": "test_token",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
            "SECRET_KEY": "test_secret_16_chars",
            "UNKNOWN_FIELD": "should_be_ignored",
            "ANOTHER_UNKNOWN": "also_ignored",
        },
        clear=True,
    ):
        # Should not raise ValidationError
        settings = Settings()
        assert settings.telegram_token == "test_token"


def test_settings_bool_conversion() -> None:
    """Test that Settings correctly converts string to bool for debug field."""
    from src.core.config import Settings

    test_cases = [
        ("True", True),
        ("true", True),
        ("False", False),
        ("false", False),
        ("1", True),
        ("0", False),
    ]

    for value, expected in test_cases:
        with patch.dict(
            os.environ,
            {
                "TELEGRAM_TOKEN": "test_token",
                "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
                "SECRET_KEY": "test_secret_16_chars",
                "DEBUG": value,
            },
            clear=True,
        ):
            settings = Settings()
            assert settings.debug is expected


def test_settings_access_token_expire_minutes_int() -> None:
    """Test that ACCESS_TOKEN_EXPIRE_MINUTES is converted to int."""
    from src.core.config import Settings

    with patch.dict(
        os.environ,
        {
            "TELEGRAM_TOKEN": "test_token",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
            "SECRET_KEY": "test_secret_16_chars",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "90",
        },
        clear=True,
    ):
        settings = Settings()
        assert isinstance(settings.access_token_expire_minutes, int)
        assert settings.access_token_expire_minutes == 90


def test_settings_secret_key_min_length() -> None:
    """Test that SECRET_KEY validates minimum length (16 characters)."""
    from src.core.config import Settings

    short_keys = ["", "short", "123456789012345"]  # Less than 16 chars

    for short_key in short_keys:
        with patch.dict(
            os.environ,
            {
                "TELEGRAM_TOKEN": "test_token",
                "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
                "SECRET_KEY": short_key,
            },
            clear=True,
        ):
            with pytest.raises(ValidationError) as exc_info:
                Settings()

            errors = exc_info.value.errors()
            assert any("SECRET_KEY" in str(error.get("loc", [])) for error in errors)

    # Valid key should pass
    with patch.dict(
        os.environ,
        {
            "TELEGRAM_TOKEN": "test_token",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test_db",
            "SECRET_KEY": "1234567890123456",  # Exactly 16 chars
        },
        clear=True,
    ):
        settings = Settings()
        assert settings.secret_key == "1234567890123456"
