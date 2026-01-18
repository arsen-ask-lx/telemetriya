### Title
Database Connection & Session Management

### Goal
Реализовать async connection pooling, session factory, dependency injection для FastAPI и graceful shutdown.

### Context
После создания миграций (task-009) нужно:
- Управлять соединениями с БД эффективно
- Обеспечить безопасную работу с сессиями
- Интегрироваться с FastAPI dependency injection
- Обрабатывать connection retry и graceful shutdown

### Scope
**In scope:**
- Создание AsyncEngine с connection pooling
- Создание SessionFactory
- Dependency injection для FastAPI (get_db)
- Graceful shutdown (close connections)
- Connection retry logic
- Health check для БД
- Unit тесты для connection pool
- Unit тесты для session lifecycle
- Integration тесты с реальной БД

**Out of scope:**
- Repository layer (task-011)

### Interfaces / Contracts
**Функции:**
```python
# src/db/session.py
async def init_db() -> None:  # инициализация connection pool
async def close_db() -> None:  # graceful shutdown
async def get_db() -> AsyncGenerator[AsyncSession, None]:  # dependency injection

# src/api/dependencies.py (если нужно)
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:  # FastAPI DI

# src/core/health.py
async def check_db_health() -> bool:  # health check
```

**Параметры connection pool:**
- pool_size: 10 (default)
- max_overflow: 20
- pool_pre_ping: True (проверка соединений)
- pool_recycle: 3600 (1 час)
- echo: False (prod), True (dev)

### Plan (маленькими шагами)
1) Написать тест для init_db функции
2) Создать src/db/session.py с init_db()
3) Настроить AsyncEngine с connection pooling
4) Настроить SessionFactory
5) Написать тест для close_db функции
6) Реализовать close_db() для graceful shutdown
7) Написать тест для get_db dependency
8) Реализовать get_db() с AsyncGenerator для FastAPI
9) Написать тест для connection pool parameters
10) Настроить pool_size, max_overflow, pool_pre_ping, pool_recycle
11) Написать тест для connection retry logic
12) Реализовать connection retry с exponential backoff
13) Написать тест для health check
14) Создать check_db_health() функцию
15) Создать FastAPI lifespan events для init_db/close_db
16) Интегрировать с FastAPI app (если уже создан) или заглушку
17) Написать integration тесты с реальной БД
18) Проверить session lifecycle (create, commit, rollback, close)
19) Проверить connection reuse (pooling)
20) Запустить все тесты

### Tests / Evals (измерение)
**Existing:**
- Все существующие тесты должны проходить (task-001-009)

**New:**
- tests/db/session/test_init_db.py:
  - test_init_db_creates_engine
  - test_init_db_configures_pool_correctly
  - test_init_db_retry_on_connection_failure

- tests/db/session/test_close_db.py:
  - test_close_db_disposes_engine
  - test_close_db_is_idempotent

- tests/db/session/test_get_db.py:
  - test_get_db_yields_session
  - test_get_db_closes_session_after_use
  - test_get_db_handles_exception_and_rolls_back

- tests/db/session/test_pool_config.py:
  - test_pool_size_configured
  - test_max_overflow_configured
  - test_pool_pre_ping_enabled
  - test_pool_recycle_configured

- tests/db/session/test_retry_logic.py:
  - test_retry_on_connection_error
  - test_retry_with_exponential_backoff
  - test_retry_max_attempts

- tests/core/health/test_db_health.py:
  - test_db_health_returns_true_when_connected
  - test_db_health_returns_false_when_disconnected

### Files allowlist
- `src/db/session.py` (создать)
- `src/api/dependencies.py` (создать - если нужно для FastAPI DI)
- `src/core/health.py` (создать - для health check)
- `src/api/main.py` (создать или обновить - для lifespan events)
- `tests/db/session/` (создать директорию + тесты)
- `tests/core/health/` (создать директорию + тесты)
- `src/core/config.py` (обновить - если нужно добавить DB settings)

### Definition of Done (DoD)
- [ ] init_db() создана с AsyncEngine
- [ ] Connection pool настроен с правильными параметрами
- [ ] close_db() реализована для graceful shutdown
- [ ] get_db() реализован как FastAPI dependency
- [ ] Connection retry logic реализован с exponential backoff
- [ ] check_db_health() реализован
- [ ] FastAPI lifespan events интегрированы
- [ ] Все unit тесты проходят (минимум 15 тестов)
- [ ] Integration тесты с реальной БД проходят
- [ ] Session lifecycle работает корректно (create, commit, rollback, close)
- [ ] Connection pooling работает (соединения переиспользуются)
- [ ] Graceful shutdown закрывает все соединения
- [ ] Health check возвращает корректный статус
- [ ] allowlist не нарушен
- [ ] Нет секретов в коде

### Risks / Edge cases
- **Connection leaks:** сессии должны всегда закрываться (использовать finally или context manager)
- **Pool exhaustion:** max_overflow должен быть достаточным для пиковых нагрузок
- **Connection timeout:** retry logic не должен бесконечно повторяться
- **Async/await:** все операции должны быть async
- **Environment mismatch:** connection string должен быть правильным для dev/test/prod
- **Race conditions:** при shutdown может быть активные запросы

### How to verify
Команды и ожидаемый результат:

```bash
# Запуск тестов
pytest tests/db/session/ tests/core/health/ -v
# Ожидается: exit code 0, все тесты проходят

# Проверка типов
mypy src/db/session.py src/api/dependencies.py src/core/health.py
# Ожидается: no errors found

# Проверка импортов
python -c "from src.db.session import init_db, close_db, get_db; from src.core.health import check_db_health"
# Ожидается: нет ошибок импорта

# Интеграционный тест (если есть FastAPI app)
pytest tests/integration/test_db_connection.py -v
# Ожидается: exit code 0, тесты проходят

# Проверка health check (если есть endpoint)
curl http://localhost:8000/health
# Ожидается: {"status": "healthy", "database": "connected"}
```

### Handoff notes
Next agent: builder
- Убедиться, что PostgreSQL запущен (task-007 выполнен)
- Убедиться, что миграции применены (task-009 выполнен)
- Использовать SQLAlchemy 2.x async features (AsyncEngine, AsyncSession, create_async_engine)
- Database URL должен быть с async:// (например, postgresql+asyncpg://)
- Для connection pooling использовать QueuePool
- Использовать contextlib.asynccontextmanager для get_db()
- В lifespan events вызывать init_db() при startup и close_db() при shutdown
- Health check должен быть быстрым (ping query)
- Connection retry: максимум 3 попытки с экспоненциальной задержкой (1, 2, 4 секунды)
