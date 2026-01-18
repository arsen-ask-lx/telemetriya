# Project Structure Map (Flat View)
Описание архитектуры и назначения файлов проекта.

## 1. Конфигурация (Root)
* `AGENTS.md` — Глобальные правила (Конституция). Читается всеми агентами.
* `.gptignore` — Список исключений (аналог .gitignore для LLM).
* `.github/workflows/ci.yml` — GitHub Actions CI/CD pipeline (lint, typecheck, tests jobs).
* `.gitignore` — Git исключения (Python, secrets, cache, venv, node_modules, *.db).
* `.gitattributes` — Git настройки (line endings LF, LFS для больших файлов).
* `README.md` — Документация проекта (описание, установка, запуск).
* `LICENSE` — MIT лицензия.
* `CONTRIBUTING.md` — Правила контрибьюции (Conventional Commits, TDD, Code of Conduct).
* `CHANGELOG.md` — Журнал изменений (Keep a Changelog format).
* `requirements.txt` — Production зависимости (Python пакеты).
* `requirements-dev.txt` — Development зависимости (тестирование, линтинг, типизация).
* `pyproject.toml` — Конфигурация инструментов (ruff, pytest, mypy, coverage).

## 2. Спецификации и Память (specs/)
**Docs (Общее)**
* `specs/docs/vision.md` — Исходное видение проекта (черновики идей).
* `specs/docs/plan.md` — Глобальный план развития проекта (Roadmap).

**Evals (Контроль качества)**
* `specs/evals/cases.jsonl` — "Золотой датасет". Примеры Input -> Expected Output.
* `specs/evals/run_eval.py` — Скрипт для автоматического прогона тестов.
* `specs/evals/verify_git_setup.py` — Проверочный скрипт для task-001 (TDD RED phase).
* `specs/evals/verify_venv_setup.py` — Проверочный скрипт для task-002 (создан builder).

**Memory (Контекст RCF)**
* `specs/memory/activeContext.md` — Оперативная память. Текущий статус задачи и фокус.
* `specs/memory/lessons.md` — Журнал ошибок и выводов (Learning Log).
* `specs/memory/structure.md` — ЭТОТ ФАЙЛ. Карта путей.

**Tasks (Рабочее пространство)**
* `specs/tasks/task-001-git-github-setup/task.md` — Task-001 (COMPLETED): Git & GitHub Setup.
* `specs/tasks/task-002-virtual-env-setup/task.md` — Task-002 (COMPLETED): Virtual Environment Setup.
* `specs/tasks/task-003-project-structure/task.md` — Task-003 (COMPLETED): Project Structure Setup.
* `specs/tasks/task-004-config-management/task.md` — Task-004 (COMPLETED): Configuration Management.
* `specs/tasks/task-005-logging-setup/task.md` — Task-005 (COMPLETED): Logging Setup.
* `specs/tasks/task-006-github-actions-cicd/task.md` — Task-006 (COMPLETED): GitHub Actions CI/CD.

## 3. Инструментарий агента (.opencode/)
* `.opencode/agents/breaker.md` — Промпт для роли Планировщика.
* `.opencode/agents/builder.md` — Промпт для роли Разработчика.
* `.opencode/agents/reviewer.md` — Промпт для роли Ревьюера.
* `.opencode/agents/archivist.md` — Промпт для роли Документатора.

## 4. Исходный код (src/)
**Core (src/core/)**
* `src/core/__init__.py` — Core package (экспортирует get_settings, Settings, setup_logging, get_logger).
* `src/core/config.py` — Pydantic Settings v2 configuration management с field_validator для SECRET_KEY.
* `src/core/logging.py` — Structured logging with PIIFormatter (JSON with PII masking), TextFormatter (colored console), setup_logging(), get_logger().

**Database (src/db/)**
* `src/db/__init__.py` — Database package.
* `src/db/models/__init__.py` — SQLAlchemy models (User, Note, Reminder, etc.).
* `src/db/repositories/__init__.py` — Repository layer (CRUD operations).

**Bot (src/bot/)**
* `src/bot/__init__.py` — Telegram bot package.
* `src/bot/handlers/__init__.py` — Command/message handlers (/start, /help, text, voice, etc.).
* `src/bot/middlewares/__init__.py` — Bot middleware (logging, error handling, user context).
* `src/bot/keyboards/__init__.py` — Inline/Reply keyboards.

**API (src/api/)**
* `src/api/__init__.py` — FastAPI application.
* `src/api/v1/__init__.py` — API v1 endpoints.
* `src/api/v1/schemas/__init__.py` — Pydantic schemas (request/response DTOs).
* `src/api/v1/endpoints/__init__.py` — API endpoints (/v1/users, /v1/notes, etc.).
* `src/api/v1/middleware/__init__.py` — API middleware (auth, rate limiting, logging).

**LLM (src/llm/)**
* `src/llm/__init__.py` — LLM integration package.
* `src/llm/clients/__init__.py` — LLM clients (Ollama, GLM-4.7, OpenAI/Gemini).
* `src/llm/schemas/__init__.py` — Pydantic schemas for LLM outputs (intent, classification, tagging).
* `src/llm/prompts/__init__.py` — Prompt templates.

**Storage (src/storage/)**
* `src/storage/__init__.py` — File storage package.

**Integrations (src/integrations/)**
* `src/integrations/__init__.py` — External integrations package.
* `src/integrations/todoist/__init__.py` — Todoist integration (MCP client, sync).

**Utils (src/utils/)**
* `src/utils/__init__.py` — Utility functions (datetime, validation, etc.).

## 5. Тесты (tests/)
* `tests/__init__.py` — Tests package.
* `tests/unit/test_logging.py` — Unit tests for logging module (PII masking, formatters, dev/prod mode).
* `tests/unit/test_config.py` — Unit tests for Pydantic Settings configuration.
* `tests/unit/__init__.py` — Unit tests (business logic, models, schemas).
* `tests/integration/__init__.py` — Integration tests (API handlers, DB).
* `tests/e2e/__init__.py` — End-to-end tests (full user journeys).

## 6. Инфраструктура и вспомогательные директории
* `docs/.gitkeep` — Documentation directory.
* `scripts/.gitkeep` — Helper scripts (docker-up.sh/down.sh/logs.sh/exec.sh, docker-up.bat/down.bat/logs.bat/exec.bat).
* `storage/pdf/.gitkeep` — PDF files storage.
* `storage/voice/.gitkeep` — Voice messages storage.
* `storage/temp/.gitkeep` — Temporary files storage.
* `infra/docker/docker-compose.yml` — Docker Compose configuration (PostgreSQL 16 + pgvector).
* `infra/postgres/init.sql` — PostgreSQL initialization script (pgvector + uuid-ossp extensions).
* `infra/monitoring/.gitkeep` — Monitoring configs (Prometheus, Grafana).
* `infra/secrets/.gitkeep` — Secrets management (templates, no actual secrets).
* `tests/docker/__init__.py` — Docker configuration tests package.
* `tests/docker/test_docker_compose.py` — Tests for docker-compose.yml validation.
* `tests/docker/test_scripts.py` — Tests for Docker management scripts.
