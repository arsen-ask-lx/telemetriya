### Title
Docker + PostgreSQL 16 with pgvector extension

### Goal
Настроить Docker Compose для PostgreSQL 16 с pgvector extension, создать скрипты управления контейнерами и обеспечить изоляцию контейнеров.

### Context
Phase 1 начинается с создания базы данных. Docker + PostgreSQL обеспечит:
- Изолированное окружение для разработки
- Легкую установку и удаление
- Возможность легко менять версию БД
- Persistent volumes для сохранения данных

### Scope
**In scope:**
- Создание docker-compose.yml с PostgreSQL 16
- Установка pgvector extension через init.sql
- Настройка health checks
- Создание persistent volumes
- Скрипты управления контейнерами (up, down, logs, exec)
- Network isolation
- Unit tests для docker-compose валидации

**Out of scope:**
- SQLAlchemy models (будет в task-008)
- Alembic migrations (будет в task-009)
- Connection pooling (будет в task-010)
- Repository layer (будет в task-011)

### Interfaces / Contracts
**Docker Compose Structure:**
- Services: postgres, (опционально) pgadmin
- Networks: telemetriya-network
- Volumes: postgres-data, pgadmin-data (опционально)
- Environment: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

**Скрипты:**
- scripts/docker-up.sh: запускает контейнеры
- scripts/docker-down.sh: останавливает контейнеры
- scripts/docker-logs.sh: показывает логи
- scripts/docker-exec.sh: открывает psql консоль

### Plan (маленькими шагами)
1) Написать тест для проверки docker-compose.yml структуры
2) Создать docker-compose.yml с PostgreSQL 16 сервисом
3) Создать infra/postgres/init.sql для установки pgvector
4) Написать тест для проверки pgvector extension установки
5) Добавить health checks в docker-compose.yml
6) Создать скрипты управления контейнерами (up, down, logs, exec)
7) Написать тесты для скриптов управления
8) Проверить запуск контейнеров и доступность БД
9) Протестировать persistent volumes (перезапуск сохраняет данные)
10) Обновить README.md с инструкциями по запуску Docker

### Tests / Evals (измерение)
**Existing:**
- Все существующие тесты должны проходить (не должно быть регрессий)

**New:**
- tests/docker/test_docker_compose.py:
  - test_docker_compose_file_exists
  - test_docker_compose_valid_yaml
  - test_postgres_service_configured
  - test_pgvector_extension_in_init_sql
  - test_health_checks_configured
  - test_volumes_configured
- tests/docker/test_scripts.py:
  - test_docker_up_script_exists
  - test_docker_down_script_exists
  - test_docker_logs_script_exists
  - test_docker_exec_script_exists

### Files allowlist
- `infra/docker/docker-compose.yml` (создать)
- `infra/postgres/init.sql` (создать)
- `scripts/docker-up.sh` (создать)
- `scripts/docker-down.sh` (создать)
- `scripts/docker-logs.sh` (создать)
- `scripts/docker-exec.sh` (создать)
- `tests/docker/` (создать директорию + тесты)
- `README.md` (обновить инструкции по Docker)
- `.env.example` (обновить с DATABASE_URL переменными)

### Definition of Done (DoD)
- [ ] docker-compose.yml создан с PostgreSQL 16 сервисом
- [ ] pgvector extension установлен через init.sql
- [ ] Health checks настроены для PostgreSQL сервиса
- [ ] Persistent volumes настроены
- [ ] Network isolation настроена
- [ ] Все скрипты управления созданы и исполняемые
- [ ] Все unit тесты проходят
- [ ] Контейнеры успешно запускаются и останавливаются
- [ ] Данные сохраняются после перезапуска (persistent volumes)
- [ ] БД доступна через psql из скриптов
- [ ] README.md обновлен с инструкциями по запуску Docker
- [ ] .env.example обновлен с DATABASE_URL примером
- [ ] allowlist не нарушен
- [ ] Нет секретов в коде

### Risks / Edge cases
- **Port conflict:** PostgreSQL порт 5432 может быть занят → использовать другой порт в .env
- **Docker не установлен:** скрипты должны проверять наличие Docker и вывести понятное сообщение
- **Windows compatibility:** скрипты должны работать и на Windows (может потребовать .bat или WSL)
- **Volume permissions:** на Linux могут быть проблемы с правами доступа к volumes
- **PostgreSQL version mismatch:** убедиться, что pgvector поддерживает выбранную версию

### How to verify
Команды и ожидаемый результат:

```bash
# Запуск контейнеров
scripts/docker-up.sh
# Ожидается: контейнеры запускаются без ошибок

# Проверка статуса
docker-compose -f infra/docker/docker-compose.yml ps
# Ожидается: postgres service "Up"

# Проверка подключения
scripts/docker-exec.sh
# Ожидается: psql консоль открывается

# Внутри psql проверить pgvector
\dx
# Ожидается: pgvector в списке extensions

# Проверка health check
docker-compose -f infra/docker/docker-compose.yml ps postgres
# Ожидается: status "healthy"

# Запуск тестов
pytest tests/docker/ -v
# Ожидается: exit code 0, все тесты проходят

# Остановка контейнеров
scripts/docker-down.sh
# Ожидается: контейнеры останавливаются, volumes сохраняются

# Повторный запуск с сохранением данных
scripts/docker-up.sh
scripts/docker-exec.sh
# Ожидается: ранее созданные данные видны
```

### Handoff notes
Next agent: builder
- Убедиться, что Docker и Docker Compose установлены на машине
- При разработке скриптов учитывать Windows (WSL) и Linux
- Добавить .env переменные для конфигурации PostgreSQL (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT)
- Тестировать persistent volumes: создать таблицу, остановить контейнер, запустить снова, проверить что таблица есть
