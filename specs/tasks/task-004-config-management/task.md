# Task: Configuration Management

## Goal
Реализовать централизованную конфигурацию с Pydantic v2 Settings, валидацией и поддержкой environment variables.

## Scope
### In Scope:
- Создание `src/core/config.py` с Pydantic Settings
- Валидация всех обязательных полей
- Поддержка environment variables
- Кэширование настроек с `@lru_cache`
- Обновление `.env.example` с комментариями
- Unit тесты для Settings validation

### Out of Scope:
- Логирование (будет в task-005-logging)
- Security hashing/passwords (будет позже)
- Advanced configuration (redis, s3) — только placeholders

## Plan (TDD: Red → Green → Refactor)

### Phase 1: Red (Tests)
1. Создать `tests/unit/test_config.py`:
   - Тест для Settings initialization
   - Тест для validation обязательных полей
   - Тест для default значений
   - Тест для environment variables
   - Тест для кэширования настроек
2. Запустить тесты: `pytest tests/unit/test_config.py -v` (все должны FAIL)

### Phase 2: Green (Implementation)
3. Создать `src/core/config.py`:
   ```python
   from pydantic_settings import BaseSettings, SettingsConfigDict
   from pydantic import Field
   from functools import lru_cache
   from typing import Optional

   class Settings(BaseSettings):
       # App
       app_name: str = "Telemetriya"
       version: str = "0.1.0"
       debug: bool = False

       # Telegram
       telegram_token: str = Field(..., validation_alias="TELEGRAM_TOKEN")
       telegram_webhook_url: Optional[str] = Field(None, validation_alias="TELEGRAM_WEBHOOK_URL")

       # Database
       db_url: str = Field(..., validation_alias="DATABASE_URL")

       # LLM
       llm_provider: str = Field(default="ollama", validation_alias="LLM_PROVIDER")
       llm_api_key: Optional[str] = Field(None, validation_alias="LLM_API_KEY")
       llm_base_url: Optional[str] = Field(None, validation_alias="LLM_BASE_URL")
       llm_model: Optional[str] = Field(None, validation_alias="LLM_MODEL")

       # Todoist
       todoist_api_key: Optional[str] = Field(None, validation_alias="TODOIST_API_KEY")

       # Storage
       storage_path: str = Field(default="./storage", validation_alias="STORAGE_PATH")

       # Security
       secret_key: str = Field(..., validation_alias="SECRET_KEY")
       algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
       access_token_expire_minutes: int = Field(default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")

       # Logging
       log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
       log_format: str = Field(default="json", validation_alias="LOG_FORMAT")

       model_config = SettingsConfigDict(
           env_file=".env",
           env_file_encoding="utf-8",
           extra="ignore"
       )

   @lru_cache
   def get_settings() -> Settings:
       return Settings()
   ```
4. Запустить тесты: `pytest tests/unit/test_config.py -v` (все должны PASS)

### Phase 3: Refactor
5. Добавить `.env.example` с комментариями:
   ```bash
   # Application
   APP_NAME=Telemetriya
   VERSION=0.1.0
   DEBUG=False

   # Telegram Bot
   TELEGRAM_TOKEN=your_telegram_token_here
   TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook

   # Database
   DATABASE_URL=postgresql+asyncpg://telemetriya:password@localhost:5432/telemetriya

   # LLM Configuration
   LLM_PROVIDER=ollama  # Options: ollama, openai, glm
   LLM_API_KEY=
   LLM_BASE_URL=http://localhost:11434
   LLM_MODEL=mistral

   # Todoist Integration (optional)
   TODOIST_API_KEY=

   # Storage
   STORAGE_PATH=./storage

   # Security
   SECRET_KEY=your_secret_key_here_change_this_in_production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Logging
   LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
   LOG_FORMAT=json  # Options: json, text
   ```
6. Создать `.env` локально (не коммитить):
   ```bash
   cp .env.example .env
   ```
7. Refactor тесты: улучшить覆盖率, добавить edge cases
8. Запустить `pytest tests/unit/test_config.py -v --cov=src/core/config --cov-report=term-missing` (должен быть ≥ 80%)

### Phase 4: Integration
9. Проверить что `get_settings()` кэширует:
   ```python
   settings1 = get_settings()
   settings2 = get_settings()
   assert settings1 is settings2
   ```
10. Commit: `git add . && git commit -m "feat: implement configuration management with Pydantic"`

## Files Allowlist
- `src/core/config.py` (новый файл)
- `tests/unit/test_config.py` (новый файл)
- `.env.example` (обновление)
- `src/core/__init__.py` (обновление — экспорт get_settings)

## Definition of Done (DoD)
- [x] `src/core/config.py` создан с Pydantic Settings
- [x] Все обязательные поля валидируются (telegram_token, db_url, secret_key)
- [x] Default значения установлены (app_name, version, debug, llm_provider)
- [x] Environment variables поддерживаются через Pydantic Field validation_alias
- [x] `get_settings()` кэшируется с `@lru_cache`
- [x] `.env.example` обновлен с комментариями для всех полей
- [x] Unit тесты созданы и проходят:
  - Settings initialization (PASS)
  - Validation обязательных полей (PASS)
  - Default значения (PASS)
  - Environment variables (PASS)
  - Кэширование настроек (PASS)
- [x] Coverage ≥ 80% для `src/core/config.py`
- [x] Type hints для всех полей
- [x] Mypy не ругается на код
- [x] Commit сделан

## Risks / Edge Cases
- **Missing .env файл:** Pydantic Settings не будет грузить переменные
- **Invalid SECRET_KEY:** нужно будет добавить валидацию длины/форматa
- **Complex validation:** Pydantic Field validation может быть сложной для некоторых типов
- **Environment priority:** Pydantic Settings может конфликтовать с системными переменными

## How to Verify
```bash
# Unit тесты
pytest tests/unit/test_config.py -v
pytest tests/unit/test_config.py --cov=src/core/config --cov-report=term-missing

# Type check
mypy src/core/config.py

# Manual проверка
python -c "from src.core.config import get_settings; settings = get_settings(); print(settings.dict())"

# Проверка кэширования
python -c "from src.core.config import get_settings; s1 = get_settings(); s2 = get_settings(); print(s1 is s2)"
```

## Dependencies
- Task 001: Git & GitHub Setup (должен быть завершён)
- Task 002: Virtual Environment Setup (должен быть завершён)
- Task 003: Project Structure Setup (должен быть завершён)

## Estimated Time
3-4 часа

## Notes
- Использовать `validation_alias` вместо `Field(alias=...)` для Pydantic v2
- `@lru_cache` кэширует Settings singleton — это безопасно так как Settings неизменяемый
- `.env` должен быть в `.gitignore`, только `.env.example` в git
- Для prod можно использовать Docker secrets или Kubernetes secrets вместо .env
