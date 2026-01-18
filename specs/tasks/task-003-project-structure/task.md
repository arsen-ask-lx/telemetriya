# Task: Project Structure Setup

## Goal
Создать стандартную структуру директорий для проекта и `__init__.py` файлы в Python пакетах.

## Scope
### In Scope:
- Создание всех директорий по стандартной структуре
- Создание `__init__.py` в каждом Python package
- Создание placeholder файлов для документации (с пустым содержимым)
- Обновление `.gitignore` с новыми путями

### Out of Scope:
- Написание фактического кода (будет позже)
- Документация в `docs/` (будет позже)
- Скрипты в `scripts/` (будут позже)

## Plan
1. Создать базовую структуру директорий:
   ```bash
   mkdir -p src/{core,db,bot,api,llm,storage,integrations,utils,bot/handlers,bot/middlewares,bot/keyboards,api/v1/{schemas,endpoints,middleware},db/models,db/repositories,llm/clients,llm/schemas,llm/prompts,integrations/todoist}
   mkdir -p tests/{unit,integration,e2e}
   mkdir -p storage/{pdf,voice,temp}
   mkdir -p scripts
   mkdir -p infra/{docker,postgres,monitoring,secrets}
   mkdir -p docs
   ```
2. Создать `__init__.py` в каждом Python package:
   - `src/__init__.py`
   - `src/core/__init__.py`
   - `src/db/__init__.py`
   - `src/db/models/__init__.py`
   - `src/db/repositories/__init__.py`
   - `src/bot/__init__.py`
   - `src/bot/handlers/__init__.py`
   - `src/bot/middlewares/__init__.py`
   - `src/bot/keyboards/__init__.py`
   - `src/api/__init__.py`
   - `src/api/v1/__init__.py`
   - `src/api/v1/schemas/__init__.py`
   - `src/api/v1/endpoints/__init__.py`
   - `src/api/v1/middleware/__init__.py`
   - `src/llm/__init__.py`
   - `src/llm/clients/__init__.py`
   - `src/llm/schemas/__init__.py`
   - `src/llm/prompts/__init__.py`
   - `src/storage/__init__.py`
   - `src/integrations/__init__.py`
   - `src/integrations/todoist/__init__.py`
   - `src/utils/__init__.py`
   - `tests/__init__.py`
   - `tests/unit/__init__.py`
   - `tests/integration/__init__.py`
   - `tests/e2e/__init__.py`
3. Создать placeholder файлы:
   - `docs/.gitkeep` (для сохранения пустой директории в git)
   - `scripts/.gitkeep`
   - `storage/pdf/.gitkeep`
   - `storage/voice/.gitkeep`
   - `storage/temp/.gitkeep`
   - `infra/docker/.gitkeep`
   - `infra/postgres/.gitkeep`
   - `infra/monitoring/.gitkeep`
   - `infra/secrets/.gitkeep`
4. Создать `.env.example` с базовым шаблоном:
   ```bash
   # App
   APP_NAME=Telemetriya
   VERSION=0.1.0
   DEBUG=False
   LOG_LEVEL=INFO
   LOG_FORMAT=json

   # Telegram
   TELEGRAM_TOKEN=your_telegram_token_here
   TELEGRAM_WEBHOOK_URL=

   # Database
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/telemetriya

   # LLM
   LLM_PROVIDER=ollama
   LLM_API_KEY=
   LLM_BASE_URL=http://localhost:11434
   LLM_MODEL=

   # Todoist
   TODOIST_API_KEY=

   # Storage
   STORAGE_PATH=./storage

   # Security
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
5. Обновить `.gitignore` с новыми путями:
   ```
   # Storage
   storage/*
   !storage/.gitkeep
   !storage/pdf/.gitkeep
   !storage/voice/.gitkeep
   !storage/temp/.gitkeep

   # Secrets
   infra/secrets/*
   !infra/secrets/.gitkeep
   .env

   # Database
   *.db
   *.sqlite

   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   ```
6. Commit: `git add . && git commit -m "chore: create project structure"`

## Files Allowlist
- `src/` (новая директория и все подпапки)
- `tests/` (новая директория и все подпапки)
- `storage/` (новая директория и все подпапки)
- `scripts/` (новая директория)
- `infra/` (новая директория и все подпапки)
- `docs/` (новая директория)
- `.env.example` (новый файл)
- `.gitignore` (обновление)

## Definition of Done (DoD)
- [x] Все директории созданы по стандартной структуре
- [x] `__init__.py` существует в каждом Python package
- [x] Placeholder файлы созданы (.gitkeep)
- [x] `.env.example` создан с базовым шаблоном конфигурации
- [x] `.gitignore` обновлен с новыми путями (storage, secrets, *.db)
- [x] Структура видна через `tree` или `ls -R`
- [x] Commit сделан
- [x] Python может импортировать пакеты (тест: `python -c "import src"`)

## Risks / Edge Cases
- **Nested imports:** нужно будет настроить PYTHONPATH или использовать `python -m src`
- **Windows path separators:** использовать `/` в `.gitignore` для кроссплатформенности
- **Empty directories in git:** создать `.gitkeep` для сохранения пустых директорий

## How to Verify
```bash
# Проверка структуры
tree -L 3 -I '__pycache__|*.pyc|.venv' .
# или
find . -type d | grep -v __pycache__ | grep -v .venv | sort

# Проверка __init__.py файлов
find src tests -name "__init__.py" | sort

# Проверка Python imports
python -c "import src.core; import src.db; import src.bot; print('OK')"

# Проверка .env.example
cat .env.example

# Проверка git
git status
git log --oneline -1
```

## Dependencies
- Task 001: Git & GitHub Setup (должен быть завершён)
- Task 002: Virtual Environment Setup (должен быть завершён)

## Estimated Time
1-2 часа

## Notes
- Использовать пустой `__init__.py` (без кода) пока нет пакетов
- `.gitkeep` для сохранения пустых директорий в git
- `.env.example` в git, `.env` — в `.gitignore`
- PYTHONPATH можно настроить через `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`
