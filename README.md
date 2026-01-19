# Telemetriya

Telegram-бот для личной "памяти" — умные заметки с AI-обработкой.

## Описание проекта

Telemetriya — это "второй цифровой мозг", который помогает сохранять, индексировать и быстро находить информацию. Бот принимает различные типы контента (текст, голос, PDF-файлы) и использует AI для создания саммари, тегов, классификации и семантического поиска.

## Основные возможности (MVP)

- **Прием контента**: Текстовые сообщения, голосовые сообщения, PDF-файлы
- **AI-обработка**:
  - Автоматическое саммари PDF документов
  - Транскрибация голосовых сообщений
  - Автоматическое тегирование и классификация
  - Суммаризация статей и документов
- **Умный поиск**: Семантический поиск с фильтрами по времени ("что я кидал вчера про X?")
- **Напоминания**: Создание напоминаний естественным языком ("напомни завтра 9:00 позвонить...")
- **Интеграция с Todoist**: Создание задач, проектов и установка дедлайнов через MCP протокол

## Основные сценарии

1. Вы отправляете PDF → "Сделай саммари" → бот возвращает краткое содержание + ключевые тезисы
2. Вы пишете "Напомни завтра 9:00 позвонить..." → бот ставит напоминание
3. Вы спрашиваете "Что я скидывал вчера про ...?" → бот находит и показывает релевантное
4. Вы пересылаете пост/ссылку → бот предлагает: (а) в архив, (б) кратко объяснить, (в) сделать задачу в Todoist

## Стек технологий

- **Backend**: Python 3.11+, FastAPI
- **База данных**: PostgreSQL 15+ с pgvector extension (для векторного поиска)
- **LLM**: glm-4.7 / ollama / gemini (поддержка multiple providers)
- **Telegram Bot**: aiogram 3.x
- **Векторные эмбеддинги**: Sentence Transformers (multilingual)
- **Деплой**: Docker, GitHub Actions CI/CD

## Установка

### Требования

- Python 3.11+
- Docker и Docker Compose
- Telegram Bot Token (получить через @BotFather)

### Быстрый старт

#### 1. Клонирование репозитория

```bash
git clone https://github.com/arsen-ask-lx/telemetriya.git
cd telemetriya
```

#### 2. Запуск PostgreSQL с Docker

**Linux/Mac:**
```bash
# Запуск контейнеров
./scripts/docker-up.sh

# Проверка статуса
docker-compose -f infra/docker/docker-compose.yml ps

# Просмотр логов
./scripts/docker-logs.sh

# Подключение к PostgreSQL
./scripts/docker-exec.sh

# Остановка контейнеров (сохраняя данные)
./scripts/docker-down.sh

# Остановка с удалением данных
docker-compose -f infra/docker/docker-compose.yml down -v
```

**Windows:**
```cmd
REM Запуск контейнеров
scripts\docker-up.bat

REM Проверка статуса
docker-compose -f infra/docker/docker-compose.yml ps

REM Просмотр логов
scripts\docker-logs.bat

REM Подключение к PostgreSQL
scripts\docker-exec.bat

REM Остановка контейнеров (сохраняя данные)
scripts\docker-down.bat

REM Остановка с удалением данных
docker-compose -f infra/docker/docker-compose.yml down -v
```

#### 3. Настройка виртуального окружения

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация (Linux/Mac)
source .venv/bin/activate

# Активация (Windows)
.venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 4. Настройка переменных окружения

```bash
# Копирование шаблона
cp .env.example .env

# Редактирование .env (добавьте ваши ключи)
```

Обязательные переменные в `.env`:
```bash
# PostgreSQL
POSTGRES_USER=telemetriya
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=telemetriya
POSTGRES_PORT=5432

# Telegram (получить через @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token

# LLM (выберите провайдер)
# GLM-4.7 (z.ai)
LLM_PROVIDER=glm
GLM_API_KEY=your_api_key

# или Ollama (локальный)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# или OpenAI/Gemini
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key
```

#### 5. Запуск приложения

```bash
# Запуск бота (TODO: будет добавлено после Phase 2)
python -m src.bot.main
```

## Docker управление

### Команды управления

| Команда | Описание |
|---------|----------|
| `scripts/docker-up.sh` / `docker-up.bat` | Запуск контейнеров |
| `scripts/docker-down.sh` / `docker-down.bat` | Остановка контейнеров |
| `scripts/docker-logs.sh` / `docker-logs.bat` | Просмотр логов |
| `scripts/docker-exec.sh` / `docker-exec.bat` | Подключение к PostgreSQL |

### Проверка подключения

После запуска контейнеров вы можете подключиться к PostgreSQL:

```sql
-- Внутри psql консоли
\dx                    -- Просмотр установленных extensions
\dt                    -- Просмотр таблиц
\l                     -- Просмотр баз данных
\q                     -- Выход
```

### Persistent Volumes

Данные сохраняются в Docker volumes. Чтобы удалить данные полностью:

```bash
docker-compose -f infra/docker/docker-compose.yml down -v
```

### Database Migrations

Telemetriya uses Alembic for database schema migrations.

#### Running Migrations

**Linux/Mac:**
```bash
# Run all pending migrations (upgrade to latest version)
./scripts/migrate.sh

# Rollback last migration (downgrade one step)
./scripts/rollback.sh

# Create a new migration
./scripts/revision.sh "Add email field to users"
```

**Windows:**
Use Git Bash, WSL, or any bash-compatible terminal to run the `.sh` scripts:
```bash
# Run all pending migrations
./scripts/migrate.sh

# Rollback last migration
./scripts/rollback.sh
```

**Alternative** (directly via Python/Alembic):
```cmd
REM Run all pending migrations
alembic upgrade head

REM Rollback last migration
alembic downgrade -1
```

#### Migration Status

To check the current migration status:
```bash
alembic current
alembic history
```

#### Creating New Migrations

When making schema changes:
1. Modify the SQLAlchemy models in `src/db/models/`
2. Create a new migration: `./scripts/revision.sh "Description of changes"`
3. Review the generated migration file in `alembic/versions/`
4. Test the migration locally
5. Commit the migration file along with model changes

#### Important Notes

- Migrations are stored in `alembic/versions/` directory
- The initial migration (`dc9f11620792_initial_schema.py`) creates all tables and extensions
- Always review generated migrations before committing
- Migration should be reversible (both `upgrade()` and `downgrade()` must work)
- The `alembic_version` table tracks which migrations have been applied

### Troubleshooting

**Port 5432 already занят:**
```bash
# Измените порт в .env
POSTGRES_PORT=5433
```

**Проблемы с правами доступа (Linux):**
```bash
sudo chown -R $USER:$USER /var/lib/docker
```

**Health check не проходит:**
```bash
# Проверьте логи
docker-compose -f infra/docker/docker-compose.yml logs postgres

# Перезапустите контейнеры
./scripts/docker-down.sh
./scripts/docker-up.sh
```

**Migration connection errors on Windows:**
On Windows, if you encounter connection errors when running migrations:
1. Ensure PostgreSQL container is running: `docker-compose ps`
2. Check `.env` file has correct `DATABASE_URL`
3. Try running migrations from within Docker: `docker exec -it telemetriya-postgres bash`
4. Restart the container if needed: `docker-compose restart postgres`

**Проблемы с правами доступа (Linux):**
```bash
sudo chown -R $USER:$USER /var/lib/docker
```

**Health check не проходит:**
```bash
# Проверьте логи
docker-compose -f infra/docker/docker-compose.yml logs postgres

# Перезапустите контейнеры
./scripts/docker-down.sh
./scripts/docker-up.sh
```

## Документация

- [Vision](specs/docs/vision.md) — видение проекта и основные сценарии
- [Plan](specs/docs/plan.md) — детальный план разработки
- [Tasks](specs/tasks/) — текущие и выполненные задачи
- [Evals](specs/evals/) — тестовые кейсы для оценки качества

## Методология

Разработка ведется по методологии **TDD (Test-Driven Development)** с прогрессивным усложнением:

- **Red** → Написать падающий тест
- **Green** → Написать минимальный код
- **Refactor** → Улучшить код, сохранить зелёные тесты

Каждый коммит = работающий, тестируемый инкремент.

## Контрибьюция

Мы приветствуем вклад в проект! Пожалуйста, ознакомьтесь с [CONTRIBUTING.md](CONTRIBUTING.md) для получения информации о:

- Формате коммитов (Conventional Commits)
- Процессе разработки и review
- Code of Conduct

## Лицензия

Этот проект лицензирован под MIT License — см. файл [LICENSE](LICENSE).

## Контакты

- GitHub: https://github.com/arsen-ask-lx/telemetriya
- Issues: https://github.com/arsen-ask-lx/telemetriya/issues

## Статус

🚧 Проект в активной разработке — Фаза 1: Database Layer

**Выполнено:**
- ✅ Фаза 0: Infrastructure & Foundation (tasks 001-006)
- ✅ Git & GitHub Setup
- ✅ Virtual Environment Setup
- ✅ Project Structure Setup
- ✅ Configuration Management (Pydantic Settings)
- ✅ Logging Setup (PII masking)
- ✅ GitHub Actions CI/CD

**В процессе:**
- ⏳ Фаза 1: Database Layer (tasks 007-011)
- 🔄 Docker + PostgreSQL + pgvector (task-007)

**Планируется:**
- 📋 Фаза 2: Basic Telegram Bot
- 📋 Фаза 3: FastAPI Backend & API
- 📋 Фаза 4: Search & Vector Embeddings
- 📋 Фаза 5: AI Features - Part 1
- 📋 Фаза 6: AI Features - Part 2
- 📋 Фаза 7: Reminders & Tasks
- 📋 Фаза 8: Todoist Integration
- 📋 Фаза 9: Production Deployment
