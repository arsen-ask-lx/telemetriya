### Title
SQLAlchemy Models & Base Classes

### Goal
Создать SQLAlchemy модели (User, Note, Reminder, TodoistTask, Session) с полным type hinting, индексами и mixin-классами для общих полей.

### Context
После настройки PostgreSQL (task-007) нужно создать ORM модели. SQLAlchemy обеспечит:
- Типизацию и autocomplete в IDE
- Автоматическую генерацию миграций
- Валидацию данных
- Читаемый код вместо сырых SQL

### Scope
**In scope:**
- Создание Base declarative class
- Создание mixin-классов (TimestampMixin, UUIDMixin, SoftDeleteMixin)
- Создание моделей: User, Note, Reminder, TodoistTask, Session
- Pydantic schemas для всех моделей (pydantic-marshmallow или ручные)
- Индексы для часто запрашиваемых полей
- Unit тесты для всех моделей (валидация, методы)

**Out of scope:**
- Alembic миграции (будет в task-009)
- Connection management (будет в task-010)
- Repository layer (будет в task-011)

### Interfaces / Contracts
**Mixin Classes:**
- `TimestampMixin`: created_at (DateTime), updated_at (DateTime)
- `UUIDMixin`: id (UUID, primary_key)
- `SoftDeleteMixin`: deleted_at (Optional[DateTime])

**Models:**
```python
# User
- id: UUID (PK)
- telegram_id: BigInteger (unique)
- username: Optional[str]
- first_name: Optional[str]
- last_name: Optional[str]
- language_code: Optional[str]
- is_active: bool
- created_at, updated_at, deleted_at

# Note
- id: UUID (PK)
- user_id: UUID (FK -> User.id)
- content: Text
- content_type: Enum (text, voice, pdf, image)
- source: Enum (telegram, api)
- file_path: Optional[str]
- summary: Optional[Text]
- tags: Optional[ARRAY[str]]
- vector_embedding: Optional[Vector(1536)]  # pgvector
- metadata: JSONB
- created_at, updated_at, deleted_at

# Reminder
- id: UUID (PK)
- user_id: UUID (FK -> User.id)
- note_id: Optional[UUID] (FK -> Note.id)
- remind_at: DateTime
- message: Text
- is_sent: bool
- created_at, updated_at, deleted_at

# TodoistTask
- id: UUID (PK)
- user_id: UUID (FK -> User.id)
- note_id: Optional[UUID] (FK -> Note.id)
- todoist_task_id: BigInteger (external ID)
- todoist_project_id: Optional[BigInteger]
- content: Text
- due_datetime: Optional[DateTime]
- is_completed: bool
- sync_status: Enum (pending, synced, error)
- created_at, updated_at, deleted_at

# Session
- id: UUID (PK)
- user_id: UUID (FK -> User.id)
- context: JSONB
- state: Optional[str]
- last_activity: DateTime
- created_at, updated_at, deleted_at
```

### Plan (маленькими шагами)
1) Написать тест для Base class
2) Создать src/db/base.py с Base declarative class
3) Написать тесты для mixin-классов
4) Создать TimestampMixin
5) Создать UUIDMixin
6) Создать SoftDeleteMixin
7) Написать тест для User model
8) Создать User model в src/db/models/user.py
9) Написать тест для Note model
10) Создать Note model в src/db/models/note.py
11) Написать тест для Reminder model
12) Создать Reminder model в src/db/models/reminder.py
13) Написать тест для TodoistTask model
14) Создать TodoistTask model в src/db/models/todoist_task.py
15) Написать тест для Session model
16) Создать Session model в src/db/models/session.py
17) Создать __init__.py для экспорта всех моделей
18) Создать Pydantic schemas для всех моделей (опционально)
19) Запустить mypy для проверки типов
20) Запустить все тесты

### Tests / Evals (измерение)
**Existing:**
- Все существующие тесты должны проходить (task-001-007)

**New:**
- tests/db/models/test_base.py:
  - test_base_is_declarative_base
  - test_base_has_metadata

- tests/db/models/test_mixins.py:
  - test_timestamp_mixin_fields
  - test_uuid_mixin_fields
  - test_soft_delete_mixin_fields
  - test_mixins_work_together

- tests/db/models/test_user.py:
  - test_user_model_creation
  - test_user_telegram_id_unique
  - test_user_fields_validation
  - test_user_relationships

- tests/db/models/test_note.py:
  - test_note_model_creation
  - test_note_content_type_enum
  - test_note_tags_array
  - test_note_vector_embedding_field
  - test_note_metadata_jsonb
  - test_note_user_relationship

- tests/db/models/test_reminder.py:
  - test_reminder_model_creation
  - test_reminder_datetime_validation
  - test_reminder_user_relationship
  - test_reminder_note_relationship_optional

- tests/db/models/test_todoist_task.py:
  - test_todoist_task_model_creation
  - test_todoist_task_sync_status_enum
  - test_todoist_task_user_relationship
  - test_todoist_task_note_relationship_optional

- tests/db/models/test_session.py:
  - test_session_model_creation
  - test_session_context_jsonb
  - test_session_user_relationship
  - test_session_state_optional

### Files allowlist
- `src/db/base.py` (создать)
- `src/db/models/` (создать директорию)
- `src/db/models/__init__.py` (создать)
- `src/db/models/user.py` (создать)
- `src/db/models/note.py` (создать)
- `src/db/models/reminder.py` (создать)
- `src/db/models/todoist_task.py` (создать)
- `src/db/models/session.py` (создать)
- `src/db/schemas/` (создать директорию - опционально)
- `src/db/schemas/__init__.py` (создать - опционально)
- `src/db/schemas/user.py` (создать - опционально)
- `src/db/schemas/note.py` (создать - опционально)
- `src/db/schemas/reminder.py` (создать - опционально)
- `src/db/schemas/todoist_task.py` (создать - опционально)
- `src/db/schemas/session.py` (создать - опционально)
- `tests/db/models/` (создать директорию + тесты)

### Definition of Done (DoD)
- [ ] Base declarative class создан
- [ ] Все 3 mixin-класса созданы (Timestamp, UUID, SoftDelete)
- [ ] User модель создана с правильными полями
- [ ] Note модель создана с правильными полями (включая vector_embedding)
- [ ] Reminder модель создана с правильными полями
- [ ] TodoistTask модель создана с правильными полями
- [ ] Session модель создана с правильными полями
- [ ] Все поля имеют правильные типы и ограничения (unique, nullable, defaults)
- [ ] Индексы созданы для часто запрашиваемых полей
- [ ] Pydantic схемы созданы (если применимо)
- [ ] Все unit тесты проходят (минимум 20 тестов)
- [ ] mypy не показывает ошибок типов
- [ ] Все модели импортируются через src/db/models/__init__.py
- [ ] allowlist не нарушен
- [ ] Нет секретов в коде

### Risks / Edge cases
- **pgvector type:** нужно убедиться, что PostgreSQL pgvector extension установлен (зависит от task-007)
- **Enum values:** content_type и sync_status должны быть хорошо определены
- **JSONB validation:** metadata и context поля должны быть валидны
- **Foreign key cascades:** определить поведение при удалении пользователя (CASCADE или RESTRICT)
- **Vector dimension:** 1536 для OpenAI embeddings, но если будем использовать другой провайдер - нужно будет изменить

### How to verify
Команды и ожидаемый результат:

```bash
# Запуск тестов
pytest tests/db/models/ -v
# Ожидается: exit code 0, все тесты проходят

# Проверка типов
mypy src/db/
# Ожидается: no errors found

# Проверка импортов
python -c "from src.db.models import User, Note, Reminder, TodoistTask, Session"
# Ожидается: нет ошибок импорта

# Проверка метаданных
python -c "from src.db.models import Base; print(Base.metadata.tables.keys())"
# Ожидается: список всех таблиц
```

### Handoff notes
Next agent: builder
- Убедиться, что PostgreSQL контейнер запущен (task-007 выполнен)
- Использовать SQLAlchemy 2.x (async support)
- Vector field: нужно использовать `pgvector.sqlalchemy.Vector` или пользовательский тип
- Enum использовать с sqlalchemy.Enum для PostgreSQL
- JSONB использовать sqlalchemy.types.JSONB или sqlalchemy.JSON
- При создании индексов использовать Index() из sqlalchemy
