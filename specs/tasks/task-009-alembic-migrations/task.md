### Title
Alembic Migrations Setup

### Goal
Настроить Alembic для управления версиями схемы базы данных, создать первую миграцию с начальной схемой (все модели из task-008).

### Context
После создания моделей (task-008) нужно:
- Создать систему миграций для evolutionary database changes
- Обеспечить возможность upgrade/downgrade схемы
- Создать первую миграцию с pgvector extension

### Scope
**In scope:**
- Установка и настройка Alembic
- Создание alembic.ini конфигурации
- Создание env.py с async support
- Создание первой миграции (initial schema)
- Создание скриптов для управления миграциями (migrate.sh, rollback.sh, revision.sh)
- Unit тесты для миграционного runner
- Тестирование upgrade/downgrade

**Out of scope:**
- Connection management (task-010)
- Repository layer (task-011)

### Interfaces / Contracts
**Скрипты:**
- scripts/migrate.sh: запускает alembic upgrade head
- scripts/rollback.sh: запускает alembic downgrade -1
- scripts/revision.sh: создает новую миграцию (с параметром message)

**Структура миграций:**
- versions/: папка с миграциями
- Каждая миграция: upgrade() и downgrade()
- Первая миграция: CREATE EXTENSION pgvector + CREATE TABLE для всех моделей

### Plan (маленькими шагами)
1) Написать тест для проверки Alembic установки
2) Установить alembic и добавить в requirements.txt
3) Запустить `alembic init alembic`
4) Настроить alembic.ini (database URL из конфига)
5) Настроить alembic/env.py (async engine support, import models)
6) Настроить alembic/script.py.mako (шаблон миграций)
7) Создать первую миграцию: `alembic revision --autogenerate -m "Initial schema"`
8) Проверить сгенерированную миграцию (ручной review)
9) Добавить pgvector extension в первую миграцию
10) Написать тест для миграции runner
11) Создать скрипт scripts/migrate.sh
12) Создать скрипт scripts/rollback.sh
13) Создать скрипт scripts/revision.sh
14) Сделать скрипты исполняемыми (chmod +x)
15) Написать тесты для скриптов (mock subprocess)
16) Протестировать upgrade на пустой БД
17) Протестировать downgrade
18) Протестировать upgrade/downgrade на существующей БД
19) Добавить документацию в миграции (комментарии)
20) Обновить README.md с инструкциями по миграциям

### Tests / Evals (измерение)
**Existing:**
- Все существующие тесты должны проходить (task-001-008)

**New:**
- tests/db/migrations/test_alembic_config.py:
  - test_alembic_directory_exists
  - test_alembic_ini_exists
  - test_env_py_exists
  - test_models_imported_in_env_py

- tests/db/migrations/test_migration_runner.py:
  - test_migration_upgrade_runs_successfully
  - test_migration_downgrade_runs_successfully
  - test_migration_idempotent (можно запустить upgrade дважды)
  - test_pgvector_extension_created

- tests/db/migrations/test_scripts.py:
  - test_migrate_script_exists
  - test_rollback_script_exists
  - test_revision_script_exists

### Files allowlist
- `alembic/` (создать директорию)
- `alembic/versions/` (создать директорию)
- `alembic.ini` (создать)
- `alembic/env.py` (создать)
- `alembic/script.py.mako` (создать)
- `requirements.txt` (обновить: добавить alembic)
- `scripts/migrate.sh` (создать)
- `scripts/rollback.sh` (создать)
- `scripts/revision.sh` (создать)
- `tests/db/migrations/` (создать директорию + тесты)
- `README.md` (обновить: секция про миграции)

### Definition of Done (DoD)
- [ ] Alembic установлен (requirements.txt обновлен)
- [ ] alembic init выполнен успешно
- [ ] alembic.ini настроен с DATABASE_URL
- [ ] alembic/env.py настроен с async support и импортом всех моделей
- [ ] alembic/script.py.mako настроен с правильным шаблоном
- [ ] Первая миграция создана через autogenerate
- [ ] Первая миграция включает CREATE EXTENSION pgvector
- [ ] Первая миграция включает CREATE TABLE для User, Note, Reminder, TodoistTask, Session
- [ ] Скрипты управления созданы и исполняемые
- [ ] Все unit тесты проходят
- [ ] Upgrade успешно создает все таблицы и расширения
- [ ] Downgrade успешно удаляет все таблицы и расширения
- [ ] README.md обновлен с инструкциями по миграциям
- [ ] allowlist не нарушен
- [ ] Нет секретов в коде

### Risks / Edge cases
- **Async support:** Alembic по умолчанию sync, нужно настроить async engine
- **Autogenerate limitations:** иногда не генерирует правильный код, нужен manual review
- **pgvector extension:** должен быть установлен в БД перед созданием таблиц
- **Database URL:** должен быть правильно настроен для prod/dev/test
- **Downgrade安全性:** downgrade должен быть безопасным и обратимым
- **Foreign keys:** порядок создания/удаления таблиц важен из-за FK constraints

### How to verify
Команды и ожидаемый результат:

```bash
# Установка зависимостей
pip install -r requirements.txt
# Ожидается: alembic установлен

# Создание первой миграции (если не создана)
alembic revision --autogenerate -m "Initial schema"
# Ожидается: новая миграция создана в alembic/versions/

# Проверка миграции
cat alembic/versions/*.py
# Ожидается: upgrade() и downgrade() методы, CREATE EXTENSION pgvector, CREATE TABLE

# Запуск миграции
scripts/migrate.sh
# Ожидается: Running upgrade..., success

# Проверка в БД
scripts/docker-exec.sh
# Ожидается: psql консоль

# Внутри psql
\dt
# Ожидается: список всех таблиц: user, note, reminder, todoist_task, session
\dx
# Ожидается: pgvector в списке extensions

# Откат миграции
scripts/rollback.sh
# Ожидается: Running downgrade..., success

# Повторный запуск миграции
scripts/migrate.sh
# Ожидается: Running upgrade..., success

# Запуск тестов
pytest tests/db/migrations/ -v
# Ожидается: exit code 0, все тесты проходят
```

### Handoff notes
Next agent: builder
- Убедиться, что модели созданы (task-008 выполнен)
- Использовать alembic==1.12.1 или выше
- В env.py использовать AsyncEngine из sqlalchemy.ext.asyncio
- Для DATABASE_URL использовать значение из конфига (Settings)
- При autogenerate проверить результат и отредактировать вручную если нужно
- В первой миграции явно указать CREATE EXTENSION IF NOT EXISTS vector
- Добавить комментарии в миграции для документации
- Тестировать на чистой БД (docker-compose down -v && up)
