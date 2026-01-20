# Project Structure Map (Flat View)
Описание архитектуры и назначения файлов проекта.

## 1. Конфигурация (Root)
* `AGENTS.md` — Глобальные правила (Конституция). Читается всеми агентами.
* `.gptignore` — Список исключений (аналог .gitignore для LLM).
* `.github/workflows/ci.yml` — GitHub Actions CI/CD pipeline (lint, typecheck, tests jobs).
* `.gitignore` — Git исключения (Python, secrets, cache, venv, node_modules, *.db).
* `.gitattributes` — Git настройки (line endings LF, LFS для больших файлов).
* `README.md` — Документация проекта (описание, установка, запуск, миграции).
* `LICENSE` — MIT лицензия.
* `CONTRIBUTING.md` — Правила контрибьюции (Conventional Commits, TDD, Code of Conduct).
* `CHANGELOG.md` — Журнал изменений (Keep a Changelog format).
* `requirements.txt` — Production зависимости (Python пакеты: alembic, asyncpg, psycopg2, sqlalchemy, etc.).
* `requirements-dev.txt` — Development зависимости (тестирование, линтинг, типизация).
* `pyproject.toml` — Конфигурация инструментов (ruff, pytest, mypy, coverage).
* `alembic.ini` — Alembic конфигурация (DATABASE_URL, script location, version path).

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
* `specs/tasks/task-007-docker-postgresql-pgvector/task.md` — Task-007 (COMPLETED): Docker + PostgreSQL 16 with pgvector.
* `specs/tasks/task-008-sqlalchemy-models-base-classes/task.md` — Task-008 (COMPLETED): SQLAlchemy Models & Base Classes.

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
* `src/core/health.py` — Health check functions (check_db_health) for database connectivity verification.

**Alembic (alembic/)**
* `alembic/env.py` — Alembic environment config (AsyncEngine support, model imports).
* `alembic/script.py.mako` — Migration template (шаблон для создания новых миграций).
* `alembic/versions/` — Миграции базы данных:
  - `alembic/versions/dc9f11620792_initial_schema.py` — Первая миграция (pgvector, uuid-ossp, CREATE TABLE User/Note/Reminder/TodoistTask/Session).

**Database (src/db/)**
* `src/db/__init__.py` — Database package.
* `src/db/base.py` — Base declarative class (DeclarativeBase).
* `src/db/mixins.py` — Mixin classes (TimestampMixin, UUIDMixin, SoftDeleteMixin).
* `src/db/session.py` — Async connection pooling (AsyncEngine), SessionFactory, init_db(), close_db(), get_db() dependency.
* `src/db/models/__init__.py` — SQLAlchemy models (User, Note, Reminder, etc.).
* `src/db/models/user.py` — User model (telegram users).
* `src/db/models/note.py` — Note model (user notes with ContentType, NoteSource enums).
* `src/db/models/reminder.py` — Reminder model (user reminders).
* `src/db/models/todoist_task.py` — TodoistTask model (Todoist sync with SyncStatus enum).
* `src/db/models/session.py` — Session model (conversation sessions).
* `src/db/repositories/__init__.py` — Repository layer (abstraction between services and database).
* `src/db/repositories/base.py` — Generic BaseRepository[T] with CRUD operations (create, get, get_or_404, update, delete, list, count), pagination (offset, limit), dynamic filtering, sorting, soft delete support.
* `src/db/repositories/user.py` — UserRepository (get_by_telegram_id, get_or_create_by_telegram_id, list_active_users).
* `src/db/repositories/note.py` — NoteRepository (list_by_user, search_by_content, list_by_content_type).
* `src/db/repositories/reminder.py` — ReminderRepository (list_by_user, list_pending, list_unsent).
* `src/db/repositories/todoist_task.py` — TodoistTaskRepository (get_by_todoist_id, list_by_sync_status, list_by_user).

**Repository Pattern (Design Note):**
- Abstraction layer between business logic (services) and database (SQLAlchemy)
- Generic BaseRepository[T] provides common CRUD operations for all models
- Specific repositories extend BaseRepository for business-specific queries
- Services use repositories for all database access (no direct SQLAlchemy queries in services)
- Type-safe with Generic[T] and TypeVar declarations
- Transaction management (commit/rollback) handled in repository layer

**Bot (src/bot/)**
* `src/bot/__init__.py` — Telegram bot package.
* `src/bot/handlers/__init__.py` — Command/message handlers (/start, /help, text, voice, etc.).
* `src/bot/middlewares/__init__.py` — Bot middleware (logging, error handling, user context).
* `src/bot/keyboards/__init__.py` — Inline/Reply keyboards.

**API (src/api/)**
* `src/api/__init__.py` — FastAPI application package.
* `src/api/main.py` — FastAPI app factory with lifespan events (init_db/close_db).
* `src/api/dependencies.py` — FastAPI dependencies (get_db_session, lifespan).
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
* `tests/integration/test_db_connection.py` — Integration tests for database connection (session lifecycle, connection reuse).
* `tests/e2e/__init__.py` — End-to-end tests (full user journeys).
* `tests/db/models/` — Database models unit tests:
  - `tests/db/models/test_base.py` — Base declarative class tests.
  - `tests/db/models/test_mixins.py` — Mixin classes tests (TimestampMixin, UUIDMixin, SoftDeleteMixin).
  - `tests/db/models/test_user.py` — User model tests.
  - `tests/db/models/test_note.py` — Note model tests (ContentType, NoteSource enums).
  - `tests/db/models/test_reminder.py` — Reminder model tests.
  - `tests/db/models/test_todoist_task.py` — TodoistTask model tests (SyncStatus enum).
  - `tests/db/models/test_session.py` — Session model tests.
* `tests/db/session/` — Database connection management unit tests:
  - `tests/db/session/test_init_db.py` — Tests for init_db() (creates engine, configures pool, retry logic).
  - `tests/db/session/test_close_db.py` — Tests for close_db() (disposes engine, idempotent).
  - `tests/db/session/test_get_db.py` — Tests for get_db() dependency (yields session, closes after use, handles exceptions).
  - `tests/db/session/test_pool_config.py` — Tests for connection pool parameters (pool_size, max_overflow, pool_pre_ping, pool_recycle).
  - `tests/db/session/test_retry_logic.py` — Tests for connection retry (exponential backoff, max attempts).
* `tests/db/migrations/` — Alembic migrations unit tests:
  - `tests/db/migrations/test_alembic_config.py` — Tests for alembic configuration.
  - `tests/db/migrations/test_migration_runner.py` — Tests for upgrade/downgrade operations.
  - `tests/db/migrations/test_scripts.py` — Tests for migration scripts (migrate.sh, rollback.sh, revision.sh).
* `tests/core/health/` — Health check unit tests:
  - `tests/core/health/test_db_health.py` — Tests for check_db_health() (returns true when connected, false when disconnected).
* `tests/db/repositories/` — Repository layer unit tests:
  - `tests/db/repositories/conftest.py` — Test fixtures for repositories (async_session, test models).
  - `tests/db/repositories/test_base_repository.py` — BaseRepository tests (28 tests: CRUD, pagination, filtering, sorting, soft delete).
  - `tests/db/repositories/test_user_repository.py` — UserRepository tests (16 tests: get_by_telegram_id, get_or_create, list_active, race condition).
  - `tests/db/repositories/test_note_repository.py` — NoteRepository tests (10 tests: list_by_user, search_by_content, list_by_content_type).
  - `tests/db/repositories/test_reminder_repository.py` — ReminderRepository tests (24 tests: list_by_user, list_pending, list_unsent).
  - `tests/db/repositories/test_todoist_task_repository.py` — TodoistTaskRepository tests (15 tests: get_by_todoist_id, list_by_sync_status, list_by_user).

## 6. Инфраструктура и вспомогательные директории
* `docs/.gitkeep` — Documentation directory.
* `scripts/.gitkeep` — Helper scripts (docker-up.sh/down.sh/logs.sh/exec.sh, docker-up.bat/down.bat/logs.bat/exec.bat).
* `scripts/migrate.sh` — Migration upgrade script (alembic upgrade head).
* `scripts/rollback.sh` — Migration downgrade script (alembic downgrade -1).
* `scripts/revision.sh` — Create new migration script (alembic revision --autogenerate -m "$1").
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
