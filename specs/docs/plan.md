# План разработки: Telemetriya (Smart Notes Bot)

**Стек:** Python + FastAPI, PostgreSQL + pgvector, LLM (glm-4.7/ollama/gemini), только русский язык

**GitHub:** https://github.com/arsen-ask-lx/telemetriya.git

**Методология:** TDD (Test-Driven Development), Progressive Complexity, Iterative Delivery

---

# 🔍 КРИТИЧЕСКИЕ УПУЩЕНИЯ ИСХОДНОГО ПЛАНА

## Технические упущения:
1. **Виртуальное окружение** — нет упоминания venv, requirements.txt, pyproject.toml
2. **Git/GitHub** — нет инициализации репозитория, `.gitignore`, workflow
3. **TDD методология** — нет explicit Red-Green-Refactor циклов, test-first подхода
4. **Конфигурация** — нет `.env` management, secrets handling
5. **Логирование** — нет structured logging, PII masking
6. **CI/CD** — нет GitHub Actions, автоматизированных проверок
7. **Error Handling** — нет retry-механизмов, graceful degradation
8. **Асинхронность** — нет explicit async/await стратегии
9. **Тестирование** — нет разделения unit/integration/e2e, mocking стратегии
10. **Документация** — нет API docs (OpenAPI/Swagger), архитектурных решений
11. **Health Checks** — нет monitoring, metrics, uptime checks
12. **Безопасность** — нет rate limiting, input validation на границах
13. **Performance** — нет кэширования, connection pooling, query optimization
14. **Deployment** — нет Docker multi-stage build, secrets management
15. **Backup/Restore** — нет стратегии бэкапов БД и файлов

## Процессные упущения:
1. **Нет прогрессии сложности** — сразу сложные вещи (AI, ML)
2. **Нет explicit TDD** — тесты не написаны до кода
3. **Нет итеративного подхода** — одна большая фаза вместо маленьких побед
4. **Нет промежуточных milestones** — нет checkpoints и deliverables
5. **Нет refactoring фаз** — код пишется, но не улучшается
6. **Нет peer review** — нет процесса проверки кода

---

# 📋 ДЕТАЛЬНЫЙ ПЛАН: ПРОГРЕССИВНЫЙ ПОДХОД + TDD

---

## ПРИНЦИПЫ

### 1. Progressive Complexity (от простого к сложному)
```
Foundation → Database → Basic Bot → API → Search → AI → Integrations → Production
```

### 2. TDD Methodology
**Каждый feature = 3 фазы:**
- **Red:** Написать падающий тест
- **Green:** Написать минимальный код
- **Refactor:** Улучшить код, сохранить зелёные тесты

### 3. Iterative Delivery
**Каждый commit = работающий, тестируемый инкремент**

### 4. Test Pyramid
```
     /\
    /E2E\       (5% - end-to-end)
   /------\
  /Integration\ (20% - API handlers, DB)
 /------------\
/   Unit Tests  \ (75% - business logic)
----------------
```

---

## ФАЗА 0: INFRASTRUCTURE & FOUNDATION (Дни 1-3)

### Цель фазы
Создать фундамент для разработки, который будет использоваться на протяжении всего проекта.

### Активности:

#### 0.1. Git & GitHub Setup (2-3 часа)
- Инициализация локального репозитория
- Добавление remote: `git remote add origin https://github.com/arsen-ask-lx/telemetriya.git`
- Создание `.gitignore` (Python, secrets, cache, *.db, .env, node_modules)
- Настройка `.gitattributes` (line endings, LFS для больших файлов)
- Создание `README.md` с инструкциями по установке и запуску
- Создание `LICENSE` (MIT или другая)
- Создание `CONTRIBUTING.md` (конвенции коммитов, Code of Conduct)
- Создание `CHANGELOG.md` (формат версионирования)

**Deliverable:** Репозиторий готов к работе, можно клонировать и начать разработку

---

#### 0.2. Virtual Environment Setup (1-2 часа)
- Создание Python 3.11+ виртуального окружения: `python -m venv .venv`
- Активация окружения (Linux/Mac: `source .venv/bin/activate`, Windows: `.venv\Scripts\activate`)
- Создание `requirements.txt` (production dependencies)
- Создание `requirements-dev.txt` (dev dependencies: pytest, ruff, mypy, coverage)
- Создание `pyproject.toml` (tool configs: pytest, ruff, mypy, coverage, isort)
- Установка зависимостей
- Проверка версий: `python --version`, `pytest --version`

**Deliverable:** Изолированное окружение с необходимыми инструментами разработки

---

#### 0.3. Project Structure Setup (1-2 часа)
- Создание директорий по стандартной структуре:
  - `src/` — весь исходный код
  - `tests/` — все тесты (unit, integration, e2e)
  - `storage/` — файлы (pdf, voice, temp)
  - `scripts/` — вспомогательные скрипты (dev.sh, test.sh, migrate.sh)
  - `infra/` — инфраструктура (Docker, PostgreSQL, Nginx configs)
  - `docs/` — техническая документация
- Создание `__init__.py` в каждом Python package
- Обновление `.gitignore` с новыми путями
- Создание `.env.example` с шаблоном конфигурации

**Deliverable:** Структура проекта готова к кодированию

---

#### 0.4. Configuration Management (3-4 часа)
**TDD approach:**
- Написать тесты для Settings validation
- Написать код Settings (Pydantic v2)
- Написать тесты для .env loading
- Написать код .env loading
- Рефакторинг: кэширование настроек, разделение dev/prod

**Активности:**
- Создание `src/core/config.py` с Pydantic Settings:
  - App settings (name, version, debug)
  - Telegram settings (token, webhook URL)
  - Database settings (URL, pool size)
  - LLM settings (provider, API key, base URL, model name)
  - Todoist settings (API key)
  - Storage settings (local path or S3 config)
  - Logging settings (level, format, path)
- Валидация всех обязательных полей
- Поддержка environment variables
- Кэширование настроек с `@lru_cache`
- Обновление `.env.example` с комментариями

**Deliverable:** Централизованная конфигурация с валидацией

---

#### 0.5. Logging Setup (2-3 часа)
**TDD approach:**
- Написать тесты для logger creation
- Написать код logger
- Написать тесты для JSON formatter
- Написать код JSON formatter
- Написать тесты для PII masking
- Написать код PII masking
- Рефакторинг: cleanup, улучшение формата

**Активности:**
- Создание `src/core/logging.py`:
  - Structured logging (JSON для prod, text для dev)
  - PII masking (emails, tokens, phone numbers)
  - Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Log rotation (по размеру и времени)
  - Context injection (user_id, request_id)
  - Колоризация для консоли
- Интеграция с конфигурацией
- Тестирование маскирования данных

**Deliverable:** Robust logging system с PII protection

---

#### 0.6. GitHub Actions CI/CD (4-5 часов)
**TDD approach:**
- Написать workflow YAML
- Тестировать локально с act
- Push и проверка в GitHub
- Рефакторинг: оптимизация шагов, кэширование

**Активности:**
- Создание `.github/workflows/`:
  - `ci.yml` — continuous integration:
    - Lint (ruff)
    - Typecheck (mypy)
    - Unit tests (pytest)
    - Coverage (pytest-cov)
    - Upload coverage to Codecov
  - `deploy.yml` — deployment (будет позже)
- Настройка CI для работы только с веткой main
- Настройка required checks для push в main
- Настройка automatic tagging

**Deliverable:** Автоматизированная проверка качества кода

---

**ФАЗА 0 DELIVERABLES:**
- ✅ Git репозиторий на GitHub
- ✅ Виртуальное окружение с зависимостями
- ✅ Структура проекта
- ✅ Конфигурация с валидацией
- ✅ Логирование с PII protection
- ✅ CI/CD pipeline

---

## ФАЗА 1: DATABASE LAYER (Дни 4-7)

### Цель фазы
Создать устойчивый слой доступа к данным с полной транзакционностью и валидацией.

### Активности:

#### 1.1. Docker + PostgreSQL + pgvector (4-6 часов)
**TDD approach:**
- Написать тесты для docker-compose healthcheck
- Создать docker-compose.yml
- Тестировать запуск контейнеров
- Рефакторинг: оптимизация ресурсов

**Активности:**
- Создание `infra/docker/docker-compose.yml`:
  - PostgreSQL 16 с pgvector extension
  - Health checks
  - Persistent volumes
  - Network isolation
  - Environment variables
- Создание `infra/postgres/init.sql`:
  - Установка pgvector extension
  - Установка uuid-ossp extension
  - Создание test database
- Написание скриптов для управления контейнерами:
  - `scripts/docker-up.sh`
  - `scripts/docker-down.sh`
  - `scripts/docker-logs.sh`
  - `scripts/docker-exec.sh`

**Deliverable:** Работающая PostgreSQL с pgvector в Docker

---

#### 1.2. SQLAlchemy Models & Base Classes (6-8 часов)
**TDD approach:**
- Написать тесты для User model
- Создать User model
- Написать тесты для Note model
- Создать Note model
- ... (все модели)
- Рефакторинг: вынос общих полей в BaseMixin

**Активности:**
- Создание `src/db/base.py`:
  - `Base` declarative base
  - `TimestampMixin` (created_at, updated_at)
  - `UUIDMixin` (id as UUID)
  - `SoftDeleteMixin` (deleted_at)
- Создание моделей в `src/db/models/`:
  - `user.py` — User модель
  - `note.py` — Note модель с vector_embedding
  - `reminder.py` — Reminder модель
  - `todoist_task.py` — TodoistTask модель
  - `session.py` — Session модель для диалогов
- Создание Pydantic schemas из моделей (pydantic-marshmallow)
- Unit тесты для каждой модели
- Type hints для всех полей
- Indexes для часто запрашиваемых полей

**Deliverable:** Полная модель данных с индексами

---

#### 1.3. Alembic Migrations (5-6 часов)
**TDD approach:**
- Написать тесты для migration runner
- Создать alembic configuration
- Тестировать upgrade/downgrade
- Рефакторинг: улучшение migration naming convention

**Активности:**
- Установка и настройка Alembic:
  - `alembic init alembic`
  - Настройка `alembic.ini`
  - Настройка `alembic/env.py` с async support
  - Настройка `alembic/script.py.mako` (шаблон миграций)
- Создание первой миграции:
  - `alembic revision --autogenerate -m "Initial schema"`
  - Ручная проверка сгенерированной миграции
  - Добавление pgvector extension
- Скрипты для управления миграциями:
  - `scripts/migrate.sh` (upgrade)
  - `scripts/rollback.sh` (downgrade)
  - `scripts/revision.sh` (create new migration)
- Тестирование миграций на пустой и существующей БД
- Documentation в комментариях миграций

**Deliverable:** Version control схемы БД

---

#### 1.4. Database Connection & Session Management (3-4 часа)
**TDD approach:**
- Написать тесты для connection pool
- Создать connection management
- Тестировать session lifecycle
- Рефакторинг: улучшение pooling settings

**Активности:**
- Создание `src/db/session.py`:
  - Async engine с connection pooling
  - Session factory
  - Dependency injection для FastAPI
  - Graceful shutdown
  - Connection retry logic
- Тестирование:
  - Connection pooling
  - Session lifecycle
  - Transaction boundaries
  - Error handling
- Настройка connection pool:
  - pool_size, max_overflow
  - pool_pre_ping
  - pool_recycle

**Deliverable:** Устойчивый connection management

---

#### 1.5. Repository Layer (8-10 часов)
**TDD approach:**
- Написать тесты для BaseRepository
- Создать BaseRepository
- Написать тесты для UserRepository
- Создать UserRepository
- ... (все репозитории)
- Рефакторинг: улучшение CRUD операций

**Активности:**
- Создание `src/db/repositories/base.py`:
  - Generic CRUD методы (create, get, update, delete, list)
  - Filter builder
  - Pagination support
  - Transaction handling
- Создание специфических репозиториев:
  - `src/db/repositories/user.py` — UserRepository
  - `src/db/repositories/note.py` — NoteRepository (с search)
  - `src/db/repositories/reminder.py` — ReminderRepository
  - `src/db/repositories/todoist_task.py` — TodoistTaskRepository
- Unit тесты для каждого метода
- Integration тесты с реальной БД
- Type hints для всех методов
- Error handling (not found, constraint violations)

**Deliverable:** Complete data access layer с тестами

---

**ФАЗА 1 DELIVERABLES:**
- ✅ PostgreSQL в Docker
- ✅ Полная модель данных
- ✅ Миграции Alembic
- ✅ Repository layer
- ✅ Full test coverage

---

## ФАЗА 2: BASIC TELEGRAM BOT (Дни 8-11)

### Цель фазы
Создать минимально рабочий Telegram бот, который может принимать и сохранять сообщения.

### Активности:

#### 2.1. aiogram Setup & Initialization (3-4 часа)
**TDD approach:**
- Написать тесты для bot initialization
- Создать bot setup
- Тестировать graceful shutdown
- Рефакторинг: улучшение error handling

**Активности:**
- Установка aiogram 3.x
- Создание `src/bot/bot.py`:
  - Bot instance creation
  - Dispatcher setup
  - Router registration
  - Middleware setup
  - Async startup/shutdown
  - Error handlers
- Создание `src/bot/middlewares/`:
  - `user_middleware.py` — создаем/обновляем пользователя
  - `logging_middleware.py` — логируем все сообщения
  - `error_middleware.py` — глобальный error handling
- Тестирование lifecycle hooks
- Тестирование middleware chaining

**Deliverable:** Работающий aiogram бот

---

#### 2.2. Basic Commands (/start, /help) (2-3 часа)
**TDD approach:**
- Написать тесты для /start response
- Реализовать /start handler
- Написать тесты для /help response
- Реализовать /help handler
- Рефакторинг: вынос текстов в отдельный модуль

**Активности:**
- Создание `src/bot/handlers/commands.py`:
  - `/start` — приветствие и вводная
  - `/help` — список команд
  - `/about` — о проекте
  - `/settings` — настройки (будет позже)
- Создание `src/bot/keyboards/`:
  - Inline клавиатуры для quick actions
  - Reply клавиатуры для навигации
- Unit тесты для каждого handler
- Integration тесты с mock bot

**Deliverable:** Базовые команды работают

---

#### 2.3. Text Message Handler (4-5 часов)
**TDD approach:**
- Написать тесты для text message processing
- Создать text message handler
- Тестировать сохранение в БД
- Рефакторинг: извлечение бизнес-логики в service

**Активности:**
- Создание `src/bot/handlers/messages.py`:
  - Обработка текстовых сообщений
  - Сохранение в БД через repository
  - Ответ пользователю
  - Error handling
- Создание `src/services/note_service.py`:
  - Business logic для создания заметки
  - Автоматическое тегирование (простая версия без AI)
  - Валидация данных
- Unit тесты для handlers
- Integration тесты с БД

**Deliverable:** Текстовые сообщения сохраняются

---

#### 2.4. Voice Message Handler (5-6 часов)
**TDD approach:**
- Написать тесты для voice message download
- Создать voice message handler
- Тестировать сохранение файла
- Рефакторинг: абстрагирование file storage

**Активности:**
- Создание `src/storage/local.py`:
  - Локальное хранение файлов
  - Проверка свободного места
  - Случайные имена файлов
  - Кэширование метаданных
- Создание `src/bot/handlers/voice.py`:
  - Скачивание voice messages
  - Сохранение в storage
  - Создание записи в БД
  - Ответ пользователю
- Unit тесты для storage
- Integration тесты с файловой системой

**Deliverable:** Голосовые сообщения сохраняются

---

#### 2.5. PDF File Handler (5-6 часов)
**TDD approach:**
- Написать тесты для PDF download
- Создать PDF handler
- Тестировать сохранение и парсинг
- Рефакторинг: улучшение error handling

**Активности:**
- Создание `src/bot/handlers/files.py`:
  - Приём PDF файлов
  - Валидация формата
  - Скачивание и сохранение
  - Парсинг метаданных (название, размер, страницы)
- Создание `src/services/pdf_service.py`:
  - Извлечение текста из PDF (pypdf)
  - Metadata extraction
  - Error handling для corrupt files
- Unit тесты для PDF parsing
- Integration тесты с реальными PDF файлами

**Deliverable:** PDF файлы принимаются и сохраняются

---

**ФАЗА 2 DELIVERABLES:**
- ✅ Работающий Telegram бот
- ✅ Текстовые сообщения сохраняются
- ✅ Голосовые сообщения сохраняются
- ✅ PDF файлы сохраняются
- ✅ Файлы хранятся локально
- ✅ Все функции покрыты тестами

---

## ФАЗА 3: FASTAPI BACKEND & API (Дни 12-15)

### Цель фазы
Создать REST API для интеграций и будущего веб-интерфейса.

### Активности:

#### 3.1. FastAPI Setup & Configuration (2-3 часа)
**TDD approach:**
- Написать тесты для FastAPI startup
- Создать FastAPI app
- Тестировать health endpoint
- Рефакторинг: улучшение middleware

**Активности:**
- Создание `src/api/main.py`:
  - FastAPI app initialization
  - CORS middleware
  - Exception handlers
  - Lifespan events
  - OpenAPI/Swagger docs
- Создание `src/api/v1/` structure
- Создание `src/api/middleware/`:
  - Auth middleware (будет позже)
  - Logging middleware
  - Rate limiting (будет позже)
- Health check endpoint `/health`
- Unit тесты для app startup

**Deliverable:** Работающий FastAPI сервер

---

#### 3.2. Pydantic Schemas for API (3-4 часа)
**TDD approach:**
- Написать тесты для schema validation
- Создать request schemas
- Создать response schemas
- Рефакторинг: улучшение error messages

**Активности:**
- Создание `src/api/v1/schemas/`:
  - `user.py` — User schemas
  - `note.py` — Note schemas (create, read, update, search)
  - `reminder.py` — Reminder schemas
  - `todoist.py` — Todoist schemas
  - `common.py` — Common schemas (pagination, error)
- Валидация на уровне Pydantic
- Type hints
- Documentation strings
- Unit тесты для всех schemas

**Deliverable:** Полные Pydantic схемы с валидацией

---

#### 3.3. CRUD API Endpoints (8-10 часов)
**TDD approach:**
- Написать тесты для GET /notes
- Реализовать GET /notes
- ... (все endpoints)
- Рефакторинг: улучшение error handling

**Активности:**
- Создание `src/api/v1/endpoints/`:
  - `users.py` — /v1/users/* (create, get, update)
  - `notes.py` — /v1/notes/* (create, get, list, update, delete, search)
  - `reminders.py` — /v1/reminders/* (create, get, list, cancel)
  - `todoist.py` — /v1/todoist/* (sync tasks)
- Регистрация endpoints в router
- Dependency injection для database session
- Pagination support
- Filtering and sorting
- Error handling (404, 422, 500)
- Integration тесты с TestClient

**Deliverable:** Full CRUD API с тестами

---

#### 3.4. Authentication & Authorization (5-6 часов)
**TDD approach:**
- Написать тесты для token generation
- Реализовать JWT токены
- Тестировать protected endpoints
- Рефакторинг: улучшение security

**Активности:**
- Создание `src/core/security.py`:
  - JWT token generation/validation
  - Password hashing (если нужно)
  - API key validation
- Создание `src/api/v1/endpoints/auth.py`:
  - `/v1/auth/login` — generate token
  - `/v1/auth/refresh` — refresh token
  - `/v1/auth/verify` — verify token
- Middleware для auth checking
- Type hints
- Security headers
- Unit и integration тесты

**Deliverable:** JWT authentication работает

---

**ФАЗА 3 DELIVERABLES:**
- ✅ FastAPI сервер работает
- ✅ Full CRUD API
- ✅ JWT authentication
- ✅ OpenAPI documentation
- ✅ Full test coverage

---

## ФАЗА 4: SEARCH & VECTOR EMBEDDINGS (Дни 16-20)

### Цель фазы
Реализовать семантический поиск с использованием векторных представлений.

### Активности:

#### 4.1. Sentence Transformers Setup (3-4 часа)
**TDD approach:**
- Написать тесты для model loading
- Загрузить модель для русского
- Тестировать embedding generation
- Рефакторинг: кэширование модели

**Активности:**
- Выбор модели для русского языка (например, `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`)
- Создание `src/llm/embeddings.py`:
  - Model loading (lazy loading)
  - Embedding generation
  - Batch processing
  - Error handling
  - Кэширование векторов
- Unit тесты для embedding
- Performance testing (time per embedding)
- Memory usage optimization

**Deliverable:** Работающий embedding генератор

---

#### 4.2. Vector Storage in pgvector (4-5 часов)
**TDD approach:**
- Написать тесты для vector storage
- Реализовать vector storage
- Тестировать similarity search
- Рефакторинг: оптимизация запросов

**Активности:**
- Обновление Note model с vector_embedding колонкой
- Миграция для добавления pgvector
- Создание `src/db/repositories/note.py` расширения:
  - `search_by_vector()` — semantic search
  - `update_vector()` — update embedding
  - `search_hybrid()` — hybrid (semantic + keywords)
- Indexing strategy (HNSW или IVFFlat)
- Unit тесты для vector operations
- Integration тесты с реальной БД
- Performance testing (query time)

**Deliverable:** Векторы хранятся в pgvector

---

#### 4.3. Search Service & API (6-8 часов)
**TDD approach:**
- Написать тесты для search endpoint
- Реализовать search endpoint
- Тестировать temporal filters
- Рефакторинг: улучшение relevance

**Активности:**
- Создание `src/services/search_service.py`:
  - Semantic search по запросу
  - Temporal filters (today, yesterday, week, month)
  - Keyword filters (по tags, content type)
  - Pagination
  - Relevance scoring
- Создание `src/bot/handlers/search.py`:
  - `/search <query>` command
  - "что я кидал вчера про X?" natural language parsing
- Создание `src/api/v1/endpoints/search.py`:
  - `/v1/search/` — search endpoint
- Evals для search quality (минимум 20 кейсов)
- Unit и integration тесты
- Performance optimization

**Deliverable:** Семантический поиск работает

---

#### 4.4. Automatic Vectorization (4-5 часов)
**TDD approach:**
- Написать тесты для auto-vectorization
- Реализовать auto-vectorization
- Тестировать async processing
- Рефакторинг: улучшение error handling

**Активности:**
- Создание `src/services/vectorizer_service.py`:
  - Автоматическое создание embedding для новых заметок
  - Async processing (background tasks)
  - Retry logic
  - Error handling
- Интеграция с Note creation flow
- Background worker (Celery или встроенный)
- Monitoring failures
- Unit и integration тесты

**Deliverable:** Все заметки автоматически векторизуются

---

**ФАЗА 4 DELIVERABLES:**
- ✅ Sentence transformers работают
- ✅ Векторы хранятся в pgvector
- ✅ Семантический поиск работает
- ✅ Temporal filters работают
- ✅ Auto-vectorization работает
- ✅ Evals pass-rate ≥ 90%

---

## ФАЗА 5: AI FEATURES - PART 1 (Дни 21-26)

### Цель фазы
Реализовать базовые AI функции с fallback на простую логику.

### Активности:

#### 5.1. LLM Client Abstraction (6-8 часов)
**TDD approach:**
- Написать тесты для LLM client interface
- Реализовать client interface
- Тестировать multiple providers
- Рефакторинг: улучшение error handling

**Активности:**
- Создание `src/llm/clients/base.py`:
  - Abstract base class
  - Unified interface (generate, chat, stream)
- Создание `src/llm/clients/ollama.py`:
  - Ollama client (httpx)
  - Support for models (llama2, mistral, etc)
- Создание `src/llm/clients/glm.py`:
  - GLM-4.7 от z.ai client
  - API integration
- Создание `src/llm/clients/openai.py`:
  - OpenAI client (или Gemini как fallback)
- Factory pattern для client selection
- Retry logic (exponential backoff)
- Timeout handling
- Unit тесты для каждого client
- Integration тесты с real APIs

**Deliverable:** Абстракция LLM клиента готова

---

#### 5.2. Structured Outputs with Pydantic (5-6 часов)
**TDD approach:**
- Написать тесты для schema validation
- Реализовать schema-guided generation
- Тестировать repair logic
- Рефакторинг: улучшение error messages

**Активности:**
- Создание `src/llm/schemas/`:
  - `intent.py` — intent classification schema
  - `classification.py` — content classification schema
  - `summary.py` — summary generation schema
  - `tagging.py` — tagging schema
  - `reminder.py` — reminder extraction schema
- Создание `src/llm/structured.py`:
  - Schema-guided generation
  - Output validation
  - Repair logic (одна попытка при валидации)
  - Error handling
- Prompt templates для каждого schema
- Unit тесты для всех schemas
- Integration тесты с LLM

**Deliverable:** Structured outputs работают

---

#### 5.3. Intent Routing with LLM (6-8 часов)
**TDD approach:**
- Написать тесты для intent classification
- Реализовать intent router
- Тестировать edge cases
- Рефакторинг: улучшение accuracy

**Активности:**
- Создание `src/llm/intent_router.py`:
  - Классификация интента сообщения:
    - Note creation
    - Search request
    - Reminder creation
    - Todoist task
    - Question/Help
  - Structured output с confidence scores
  - Fallback на простую логику
- Создание `src/llm/prompts/intent.py`:
  - Prompt template для intent classification
- Создание Evals для intent routing (минимум 50 кейсов)
  - Разные типы сообщений
  - Edge cases
  - Ambiguous queries
- Unit тесты для router
- Accuracy testing (target: ≥ 90%)

**Deliverable:** Intent routing работает

---

#### 5.4. Content Classification (5-6 часов)
**TDD approach:**
- Написать тесты для classification
- Реализовать classifier
- Тестировать accuracy
- Рефакторинг: улучшение prompts

**Активности:**
- Создание `src/llm/classifier.py`:
  - Классификация контента:
    - Article (статья)
    - Idea (идея)
    - Task (задача)
    - Reference (ссылка)
    - Note (заметка)
  - Structured output
  - Fallback на правила
- Создание `src/llm/prompts/classification.py`:
  - Prompt template для classification
- Evals для classification (минимум 30 кейсов)
- Unit тесты
- Accuracy testing (target: ≥ 85%)

**Deliverable:** Content classification работает

---

#### 5.5. Auto-tagging Service (4-5 часов)
**TDD approach:**
- Написать тесты для tagging
- Реализовать tagging service
- Тестировать relevance
- Рефакторинг: улучшение промптов

**Активности:**
- Создание `src/llm/tagger.py`:
  - Автоматическое тегирование заметок
  - Генерация 3-5 релевантных тегов
  - Structured output
  - Fallback на keyword extraction
- Создание `src/llm/prompts/tagging.py`:
  - Prompt template для tagging
- Evals для tagging (минимум 20 кейсов)
- Unit тесты
- Accuracy testing (subjective relevance)

**Deliverable:** Auto-tagging работает

---

**ФАЗА 5 DELIVERABLES:**
- ✅ LLM клиент абстракция
- ✅ Structured outputs работают
- ✅ Intent routing (≥ 90% accuracy)
- ✅ Content classification (≥ 85% accuracy)
- ✅ Auto-tagging работает
- ✅ Evals для всех AI функций

---

## ФАЗА 6: AI FEATURES - PART 2 (Дни 27-32)

### Цель фазы
Реализовать сложные AI функции (саммари PDF, транскрипция аудио).

### Активности:

#### 6.1. PDF Summary Generation (8-10 часов)
**TDD approach:**
- Написать тесты для summary generation
- Реализовать PDF summarizer
- Тестировать качество саммари
- Рефакторинг: улучшение streaming

**Активности:**
- Создание `src/llm/summarizer.py`:
  - Чанкование PDF текста (по токенам/параграфам)
  - Генерация саммари для каждого чанка
  - Агрегация и финальный саммари
  - Streaming response
  - Timeout handling
  - Memory management
- Создание `src/llm/prompts/summary.py`:
  - Prompt template для summarization
  - Chain-of-thought prompting
- Создание `src/bot/handlers/summary.py`:
  - `/pdf_summary` command
  - Inline кнопка для саммари
- Evals для summary quality (минимум 20 кейсов)
  - Критерии: не потерять главные выводы, краткость, ясность
- Unit тесты
- Integration тесты с реальными PDF
- Performance testing (target: < 30 сек для типичного PDF)

**Deliverable:** PDF саммари работает

---

#### 6.2. Voice Transcription (8-10 часов)
**TDD approach:**
- Написать тесты для transcription
- Реализовать transcriber
- Тестировать качество
- Рефакторинг: оптимизация ресурсов

**Активности:**
- Выбор transcriber:
  - Option A: openai-whisper (высокое качество, ресурсоемко)
  - Option B: faster-whisper (оптимизированная версия)
  - Option C: vosk-api (локальный, легкий)
- Создание `src/llm/transcriber.py`:
  - Транскрипция аудио
  - Улучшение качества для русского
  - Batch processing
  - Error handling
  - Async processing
- Создание `src/services/transcription_service.py`:
  - Background processing
  - Queue management
  - Progress updates
  - Error recovery
- Evals для transcription (минимум 10 кейсов)
  - Критерий: понятность текста, отсутствие артефактов
- Unit тесты
- Integration тесты с реальными аудио
- Performance optimization

**Deliverable:** Voice транскрипция работает

---

#### 6.3. Conversation Flow & UX (6-8 часов)
**TDD approach:**
- Написать тесты для conversation flow
- Реализовать flow manager
- Тестировать user journey
- Рефакторинг: улучшение UX

**Активности:**
- Создание `src/bot/conversations/`:
  - State machine для диалогов
  - Context retention
  - Conversation history
- Создание `src/bot/keyboards/`:
  - Inline клавиатуры для действий:
    - "Сделать саммари"
    - "Добавить теги"
    - "Создать задачу"
    - "Установить напоминание"
  - Context-aware клавиатуры
- Создание `src/bot/handlers/callbacks.py`:
  - Обработка inline кнопок
  - Multi-step flows
- Unit тесты для flow
- Integration тесты с mock user

**Deliverable:** Conversation flow работает

---

**ФАЗА 6 DELIVERABLES:**
- ✅ PDF саммари работает (< 30 сек)
- ✅ Voice транскрипция работает
- ✅ Conversation flow работает
- ✅ Inline клавиатуры работают
- ✅ Evals для всех функций

---

## ФАЗА 7: REMINDERS & TASKS (Дни 33-37)

### Цель фазы
Реализовать систему напоминаний и парсинг времени.

### Активности:

#### 7.1. Natural Language Time Parsing (6-8 часов)
**TDD approach:**
- Написать тесты для time parsing
- Реализовать time parser
- Тестировать edge cases
- Рефакторинг: улучшение accuracy

**Активности:**
- Создание `src/utils/datetime.py`:
  - Парсинг естественного языка:
    - "завтра 9:00"
    - "через 2 часа"
    - "в следующую среду"
    - "вечером"
  - Таймзона handling
  - Ambiguity resolution
  - Fallback на simple patterns
- Evals для time parsing (минимум 40 кейсов)
  - Разные форматы
  - Edge cases (високосный год, конец месяца)
  - Ambiguous queries
- Unit тесты
- Accuracy testing (target: ≥ 90%)

**Deliverable:** Time parsing работает

---

#### 7.2. Reminder Creation & Storage (5-6 часов)
**TDD approach:**
- Написать тесты для reminder creation
- Реализовать reminder service
- Тестировать storage
- Рефакторинг: улучшение error handling

**Активности:**
- Создание `src/services/reminder_service.py`:
  - Создание напоминания
  - Валидация времени
  - Связь с заметкой (опционально)
  - Conflict resolution
- Создание `src/bot/handlers/reminder.py`:
  - `/remind <время> <текст>` command
  - Inline кнопка "Напомнить позже"
- Обновление ReminderRepository
- Unit тесты
- Integration тесты с БД

**Deliverable:** Reminder создание работает

---

#### 7.3. Reminder Scheduler (6-8 часов)
**TDD approach:**
- Написать тесты для scheduler
- Реализовать scheduler
- Тестировать trigger logic
- Рефакторинг: улучшение reliability

**Активности:**
- Выбор scheduler:
  - Option A: APScheduler (простой, встроенный)
  - Option B: Celery (мощный, сложный)
  - Option C: asyncio loop (минималистичный)
- Создание `src/schedulers/reminder_scheduler.py`:
  - Периодическая проверка напоминаний
  - Отправка уведомлений
  - Retry logic для неудачных отправок
  - Graceful shutdown
- Создание `src/notifications/`:
  - Telegram notification service
  - Notification templates
- Monitoring failures
- Unit тесты
- Integration тесты с mock time

**Deliverable:** Reminder scheduler работает

---

**ФАЗА 7 DELIVERABLES:**
- ✅ Time parsing (≥ 90% accuracy)
- ✅ Reminder создание
- ✅ Reminder scheduler
- ✅ Уведомления отправляются
- ✅ Evals для time parsing

---

## ФАЗА 8: TODOIST INTEGRATION (Дни 38-43)

### Цель фазы
Интегрироваться с Todoist через MCP протокол.

### Активности:

#### 8.1. Todoist MCP Client (8-10 часов)
**TDD approach:**
- Написать тесты для MCP client
- Реализовать MCP client
- Тестировать все операции
- Рефакторинг: улучшение error handling

**Активности:**
- Изучение Todoist MCP specification
- Создание `src/integrations/todoist/mcp_client.py`:
  - MCP protocol implementation
  - Connection management
  - Task creation
  - Project creation
  - Deadline setting
  - Error handling
  - Retry logic
- Создание `src/integrations/todoist/api_client.py`:
  - Todoist REST API client (fallback)
  - Auth handling
- Unit тесты для client
- Integration тесты с real Todoist API
- Documentation

**Deliverable:** Todoist MCP клиент готов

---

#### 8.2. Task Creation from Notes (6-8 часов)
**TDD approach:**
- Написать тесты для task creation
- Реализовать task service
- Тестировать integration
- Рефакторинг: улучшение UX

**Активности:**
- Создание `src/integrations/todoist/task_service.py`:
  - Создание задачи из заметки
  - Установка проекта
  - Установка дедлайна
  - Обновление заметки с ссылкой на задачу
  - Error handling
- Создание `src/bot/handlers/todoist.py`:
  - `/task <текст>` command
  - Inline кнопка "Создать задачу"
- Создание `src/llm/schemas/todoist.py`:
  - Task extraction schema
- Unit тесты
- Integration тесты

**Deliverable:** Task creation работает

---

#### 8.3. Sync & Bi-directional Integration (6-8 часов)
**TDD approach:**
- Написать тесты для sync logic
- Реализовать sync service
- Тестировать bidirectional sync
- Рефакторинг: улучшение performance

**Активности:**
- Создание `src/integrations/todoist/sync_service.py`:
  - Синхронизация задач
  - Обновление статусов
  - Conflict resolution
  - Incremental sync
- Background sync worker
- Monitoring sync status
- Error recovery
- Unit тесты
- Integration тесты

**Deliverable:** Bi-directional sync работает

---

**ФАЗА 8 DELIVERABLES:**
- ✅ Todoist MCP клиент
- ✅ Task creation работает
- ✅ Bi-directional sync
- ✅ Заметки связаны с задачами

---

## ФАЗА 9: PRODUCTION DEPLOYMENT (Дни 44-48)

### Цель фазы
Подготовить проект к продакшен деплою.

### Активности:

#### 9.1. Docker Multi-stage Build (6-8 часов)
**TDD approach:**
- Написать тесты для docker image
- Создать Dockerfile
- Тестировать build
- Рефакторинг: оптимизация image size

**Активности:**
- Создание `infra/docker/Dockerfile`:
  - Multi-stage build
  - Python 3.11+ base image
  - Dependency installation
  - Code copying
  - Production optimizations
- Создание `infra/docker/docker-compose.prod.yml`:
  - PostgreSQL
  - Bot service
  - API service
  - Nginx (опционально)
  - Redis (опционально для Celery)
- Health checks
- Environment variables
- Volumes
- Networks

**Deliverable:** Docker image готов

---

#### 9.2. Secrets Management (4-5 часов)
**TDD approach:**
- Написать тесты для secrets loading
- Реализовать secrets management
- Тестировать security
- Рефакторинг: улучшение encryption

**Активности:**
- Создание `infra/secrets/`:
  - `.env.template` (без секретов)
  - Instructions for secrets
- Docker secrets support
- Environment variable validation
- Secret rotation strategy
- Documentation

**Deliverable:** Secrets management готов

---

#### 9.3. Monitoring & Logging (6-8 часов)
**TDD approach:**
- Написать тесты для logging
- Настроить monitoring
- Тестировать alerts
- Рефакторинг: улучшение visibility

**Активности:**
- Обновление `src/core/logging.py`:
  - Structured logging (JSON)
  - Log levels
  - Log rotation
  - Remote logging (ELK или Loki)
- Создание `infra/monitoring/`:
  - Prometheus configuration
  - Grafana dashboards
  - Alertmanager rules
  - Health check endpoints
- Metrics:
  - Request count/duration
  - Database query time
  - LLM API calls
  - Error rate
- Documentation

**Deliverable:** Monitoring работает

---

#### 9.4. Backup & Recovery (4-5 часов)
**TDD approach:**
- Написать тесты для backup
- Реализовать backup scripts
- Тестировать recovery
- Рефакторинг: улучшение performance

**Активности:**
- Создание `scripts/backup.sh`:
  - Database backup (pg_dump)
  - Files backup (rsync)
  - Compression
  - Encryption
- Создание `scripts/restore.sh`:
  - Database restore
  - Files restore
- Scheduled backups (cron)
- Backup retention policy
- Recovery testing
- Documentation

**Deliverable:** Backup & recovery работает

---

#### 9.5. CI/CD Pipeline Update (4-5 часов)
**TDD approach:**
- Написать тесты для deployment
- Обновить GitHub Actions
- Тестировать deployment
- Рефакторинг: улучшение speed

**Активности:**
- Обновление `.github/workflows/`:
  - `deploy.yml` — deployment pipeline
  - Build docker images
  - Push to registry
  - Deploy to production
  - Rollback strategy
- Automated tests на каждом этапе
- Manual approval gates
- Documentation

**Deliverable:** CI/CD pipeline готов

---

**ФАЗА 9 DELIVERABLES:**
- ✅ Docker image оптимизирован
- ✅ Secrets management
- ✅ Monitoring & logging
- ✅ Backup & recovery
- ✅ Automated CI/CD

---

## ФАЗА 10: FINAL MVP COMPLETION (Дни 49-50)

### Цель фазы
Завершить MVP и убедиться, что все критерии выполнены.

### Активности:

#### 10.1. Full Integration Testing (6-8 часов)
**TDD approach:**
- Написать E2E тесты
- Прогнать все тесты
- Рефакторинг: улучшение coverage

**Активности:**
- Создание `tests/e2e/`:
  - E2E тесты для ключевых сценариев:
    - Отправка текста → сохранение
    - Отправка PDF → саммари
    - Поиск "вчера про X" → результаты
    - Создание задачи → Todoist sync
  - Setup/teardown
  - Mock внешних сервисов
- Full test suite run
- Coverage analysis (target: ≥ 80%)
- Performance testing

**Deliverable:** All tests pass

---

#### 10.2. Evals & Quality Assurance (6-8 часов)
**TDD approach:**
- Прогнать все evals
- Анализировать результаты
- Улучшить качество
- Рефакторинг: оптимизация

**Активности:**
- Прогнать все eval cases:
  - Intent routing (≥ 90%)
  - Search quality (≥ 90%)
  - Time parsing (≥ 90%)
  - Summary quality (subjective)
- Bug fixes
- Performance optimization
- Documentation updates

**Deliverable:** All evals pass

---

#### 10.3. Documentation Finalization (4-5 часов)
**TDD approach:**
- Проверить документацию
- Обновить недостающие части
- Проверить links

**Активности:**
- Обновление `README.md`:
  - Полные инструкции по установке
  - Полные инструкции по запуску
  - Known issues
  - Troubleshooting
- Создание `docs/architecture.md`:
  - High-level architecture
  - Data flow
  - Component interaction
- Создание `docs/api.md`:
  - API documentation
  - Examples
- Создание `docs/development.md`:
  - Developer guide
  - Testing guide
  - Contributing guide

**Deliverable:** Documentation complete

---

**ФАЗА 10 DELIVERABLES:**
- ✅ All tests pass (≥ 80% coverage)
- ✅ All evals pass (≥ 90% pass-rate)
- ✅ Documentation complete
- ✅ MVP готов

---

# 📊 ФИНАЛЬНЫЙ MVP CHECKLIST

### Functional Requirements:
- ✅ Текстовое сообщение → структурированная заметка
- ✅ Голосовое сообщение → транскрипция → заметка
- ✅ PDF файл → саммари → заметка
- ✅ Поиск "саммари статьи, что я скинул вчера" → конкретный объект
- ✅ Создание Todoist задачи из диалога
- ✅ Напоминания с естественным языком

### Technical Requirements:
- ✅ Python 3.11+
- ✅ PostgreSQL 15+ с pgvector
- ✅ LLM провайдер (glm-4.7/ollama/gemini)
- ✅ Telegram bot (aiogram 3.x)
- ✅ FastAPI backend
- ✅ Docker containerization
- ✅ CI/CD pipeline
- ✅ Structured logging
- ✅ Secrets management

### Quality Requirements:
- ✅ All tests pass
- ✅ Coverage ≥ 80%
- ✅ Intent routing ≥ 90%
- ✅ Search quality ≥ 90%
- ✅ Time parsing ≥ 90%
- ✅ PDF summary < 30 сек
- ✅ Lint/typecheck passes

---

# 📈 РАСЧЁТ ВРЕМЕНИ

| Фаза | Дни | Доп. время | Total |
|------|-----|------------|-------|
| 0: Foundation | 3 | 1 | 4 |
| 1: Database | 4 | 1 | 5 |
| 2: Basic Bot | 4 | 1 | 5 |
| 3: API | 4 | 1 | 5 |
| 4: Search | 5 | 1 | 6 |
| 5: AI Part 1 | 6 | 2 | 8 |
| 6: AI Part 2 | 6 | 2 | 8 |
| 7: Reminders | 5 | 1 | 6 |
| 8: Todoist | 6 | 2 | 8 |
| 9: Production | 5 | 1 | 6 |
| 10: Final | 2 | 1 | 3 |
| **TOTAL** | **50** | **13** | **63** |

**Оптимистичный сценарий:** 50 дней (7 недель)
**Реалистичный сценарий:** 63 дней (9 недель)
**Пессимистичный сценарий:** 80 дней (11+ недель)

---

# 🎯 КЛЮЧЕВЫЕ ПРИНЦИПЫ (НАПOMИНАНИЕ)

1. **TDD First** — всегда Red → Green → Refactor
2. **Прогрессивная сложность** — от простого к сложному
3. **Test Pyramid** — 75% unit, 20% integration, 5% e2e
4. **Every commit = working increment** — всегда рабочий код
5. **Continuous Integration** — все проверки автоматизированы
6. **Documentation** — код объясняется, не только работает
7. **Security** — секреты защищены, PII маскируется
8. **Performance** — измеряется, оптимизируется
9. **Monitoring** — всё видно, всё логируется
10. **Iterative Delivery** — маленькие победы, быстрая обратная связь

---

# 🚀 ГИТХАБ & ДЕПЛОЙ

- **Repository:** https://github.com/arsen-ask-lx/telemetriya.git
- **Remote add:** `git remote add origin https://github.com/arsen-ask-lx/telemetriya.git`
- **Push:** `git push -u origin main`

---

---

**Дата создания:** 2026-01-18  
**Версия:** 1.0  

## Approval / Статус документа (Plan-first gate)

**Статус:**  
- **Approved (Phase 0 only)** — разрешено выполнять задачи фазы 0 (Foundation) по этому плану  
- **Draft (Phase 1+)** — фазы 1+ считаются черновиком и требуют отдельного owner-approval перед началом

**Approved scope:** Phase 0 — Infrastructure & Foundation (tasks 001–006)  
**Approved by:** owner  
**Approved on:** 2026-01-18  

**Правило изменения:** любые правки, влияющие на scope/последовательность фаз, требуют обновления этого блока (новая дата/объём аппрува).

---
