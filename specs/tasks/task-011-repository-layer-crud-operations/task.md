### Title
Repository Layer with CRUD Operations

### Goal
Создать Generic BaseRepository и специфические репозитории (User, Note, Reminder, TodoistTask) с CRUD операциями, пагинацией, фильтрами и полной транзакционностью.

### Context
После настройки connection management (task-010) нужно:
- Создать abstraction layer для доступа к данным
- Обеспечить type-safe CRUD операции
- Реализовать специфичные методы для бизнес-логики
- Покрыть все операции тестами

### Scope
**In scope:**
- Создание Generic BaseRepository
- CRUD методы: create, get, get_or_404, update, delete, list
- Filter builder для динамических запросов
- Pagination support
- Transaction handling
- UserRepository (специфичные методы для User)
- NoteRepository (с методами для search по vector)
- ReminderRepository (по user_id, remind_at)
- TodoistTaskRepository (по sync_status)
- Unit тесты для всех методов
- Integration тесты с реальной БД

**Out of scope:**
- Vector search implementation (будет в Phase 4)
- Business logic services (будут позже)

### Interfaces / Contracts
**BaseRepository:**
```python
class BaseRepository(Generic[T]):
    async def create(self, obj: T) -> T
    async def get(self, id: UUID) -> Optional[T]
    async def get_or_404(self, id: UUID) -> T
    async def update(self, id: UUID, updates: dict) -> T
    async def delete(self, id: UUID) -> None
    async def list(
        self,
        offset: int = 0,
        limit: int = 100,
        filters: dict = {},
        order_by: Optional[str] = None
    ) -> List[T]
    async def count(self, filters: dict = {}) -> int
```

**UserRepository:**
```python
class UserRepository(BaseRepository[User]):
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]
    async def get_or_create_by_telegram_id(
        self, telegram_id: int, **kwargs
    ) -> User
    async def list_active_users(self, offset: int, limit: int) -> List[User]
```

**NoteRepository:**
```python
class NoteRepository(BaseRepository[Note]):
    async def list_by_user(
        self, user_id: UUID, offset: int, limit: int
    ) -> List[Note]
    async def search_by_content(
        self, user_id: UUID, query: str, offset: int, limit: int
    ) -> List[Note]
    async def list_by_content_type(
        self, user_id: UUID, content_type: ContentType, offset: int, limit: int
    ) -> List[Note]
    # search_by_vector будет в Phase 4
```

**ReminderRepository:**
```python
class ReminderRepository(BaseRepository[Reminder]):
    async def list_by_user(
        self, user_id: UUID, offset: int, limit: int
    ) -> List[Reminder]
    async def list_pending(
        self, before: datetime, offset: int, limit: int
    ) -> List[Reminder]
    async def list_unsent(
        self, user_id: UUID, offset: int, limit: int
    ) -> List[Reminder]
```

**TodoistTaskRepository:**
```python
class TodoistTaskRepository(BaseRepository[TodoistTask]):
    async def get_by_todoist_id(
        self, todoist_task_id: int
    ) -> Optional[TodoistTask]
    async def list_by_sync_status(
        self, sync_status: SyncStatus, offset: int, limit: int
    ) -> List[TodoistTask]
    async def list_by_user(
        self, user_id: UUID, offset: int, limit: int
    ) -> List[TodoistTask]
```

### Plan (маленькими шагами)
1) Написать тест для BaseRepository.create()
2) Создать src/db/repositories/base.py с BaseRepository
3) Реализовать create() метод
4) Написать тест для BaseRepository.get()
5) Реализовать get() метод
6) Написать тест для BaseRepository.get_or_404()
7) Реализовать get_or_404() метод
8) Написать тест для BaseRepository.update()
9) Реализовать update() метод
10) Написать тест для BaseRepository.delete()
11) Реализовать delete() метод
12) Написать тест для BaseRepository.list() с пагинацией
13) Реализовать list() метод с offset, limit, filters, order_by
14) Написать тест для BaseRepository.count()
15) Реализовать count() метод
16) Создать UserRepository
17) Реализовать get_by_telegram_id()
18) Реализовать get_or_create_by_telegram_id()
19) Реализовать list_active_users()
20) Создать NoteRepository
21) Реализовать list_by_user()
22) Реализовать search_by_content()
23) Реализовать list_by_content_type()
24) Создать ReminderRepository
25) Реализовать list_by_user()
26) Реализовать list_pending()
27) Реализовать list_unsent()
28) Создать TodoistTaskRepository
29) Реализовать get_by_todoist_id()
30) Реализовать list_by_sync_status()
31) Реализовать list_by_user()
32) Создать src/db/repositories/__init__.py для экспорта
33) Написать интеграционные тесты с реальной БД
34) Запустить все тесты

### Tests / Evals (измерение)
**Existing:**
- Все существующие тесты должны проходить (task-001-010)

**New:**
- tests/db/repositories/test_base_repository.py:
  - test_create_returns_created_object
  - test_get_returns_object_by_id
  - test_get_returns_none_for_nonexistent_id
  - test_get_or_404_returns_object
  - test_get_or_404_raises_not_found
  - test_update_modifies_object
  - test_update_raises_not_found
  - test_delete_removes_object
  - test_delete_raises_not_found
  - test_list_returns_paginated_results
  - test_list_filters_correctly
  - test_list_sorts_correctly
  - test_count_returns_correct_count

- tests/db/repositories/test_user_repository.py:
  - test_get_by_telegram_id_returns_user
  - test_get_by_telegram_id_returns_none
  - test_get_or_create_by_telegram_id_creates_new_user
  - test_get_or_create_by_telegram_id_returns_existing
  - test_list_active_users_filters_correctly

- tests/db/repositories/test_note_repository.py:
  - test_list_by_user_filters_correctly
  - test_search_by_content_returns_matching_notes
  - test_search_by_content_returns_empty_for_no_match
  - test_list_by_content_type_filters_correctly

- tests/db/repositories/test_reminder_repository.py:
  - test_list_by_user_filters_correctly
  - test_list_pending_filters_by_datetime
  - test_list_unsent_filters_by_is_sent

- tests/db/repositories/test_todoist_task_repository.py:
  - test_get_by_todoist_id_returns_task
  - test_get_by_todoist_id_returns_none
  - test_list_by_sync_status_filters_correctly
  - test_list_by_user_filters_correctly

### Files allowlist
- `src/db/repositories/` (создать директорию)
- `src/db/repositories/__init__.py` (создать)
- `src/db/repositories/base.py` (создать)
- `src/db/repositories/user.py` (создать)
- `src/db/repositories/note.py` (создать)
- `src/db/repositories/reminder.py` (создать)
- `src/db/repositories/todoist_task.py` (создать)
- `tests/db/repositories/` (создать директорию + тесты)

### Definition of Done (DoD)
- [ ] BaseRepository создан с Generic[T]
- [ ] Все CRUD методы реализованы (create, get, get_or_404, update, delete, list, count)
- [ ] Пагинация работает (offset, limit)
- [ ] Фильтрация работает (filters dict)
- [ ] Сортировка работает (order_by)
- [ ] UserRepository создан с 3 методами
- [ ] NoteRepository создан с 3 методами
- [ ] ReminderRepository создан с 3 методами
- [ ] TodoistTaskRepository создан с 3 методами
- [ ] Все репозитории импортируются через src/db/repositories/__init__.py
- [ ] Все unit тесты проходят (минимум 35 тестов)
- [ ] Интеграционные тесты с реальной БД проходят
- [ ] Методы правильно обрабатывают not found (raise или return None)
- [ ] Транзакции работают корректно (commit, rollback)
- [ ] Type hints для всех методов
- [ ] mypy не показывает ошибок типов
- [ ] allowlist не нарушен
- [ ] Нет секретов в коде

### Risks / Edge cases
- **Generic typing:** нужно правильно настроить TypeVar для Generic[T]
- **Soft delete:** delete() должен делать soft delete если применимо
- **Pagination:** offset и limit должны быть валидированы (offset >= 0, limit > 0)
- **SQL injection:** filters должны быть безопасными (использовать SQLAlchemy expressions)
- **Concurrent updates:** update() должен использовать optimistic locking если нужно
- **N+1 queries:** list() должен использовать eager loading для отношений
- **Error handling:** все методы должны обрабатывать DBError и логировать ошибки

### How to verify
Команды и ожидаемый результат:

```bash
# Запуск тестов
pytest tests/db/repositories/ -v
# Ожидается: exit code 0, все тесты проходят

# Проверка типов
mypy src/db/repositories/
# Ожидается: no errors found

# Проверка импортов
python -c "from src.db.repositories import UserRepository, NoteRepository, ReminderRepository, TodoistTaskRepository"
# Ожидается: нет ошибок импорта

# Проверка покрытия
pytest tests/db/repositories/ --cov=src/db/repositories --cov-report=term-missing
# Ожидается: coverage >= 90%
```

### Handoff notes
Next agent: builder
- Убедиться, что connection management настроен (task-010 выполнен)
- Использовать Generic из typing для BaseRepository[T]
- Для фильтрации использовать sqlalchemy.orm.attributes InstrumentedAttribute
- Для сортировки использовать order_by clause с валидацией поля
- Для update использовать stmt.update() вместо setattr для atomicity
- Для delete использовать soft delete если модель имеет deleted_at поле
- В list() использовать options(selectinload/eagerload) для отношений
- В get_or_create() использовать try/except для race conditions
- Все асинхронные операции должны быть async/await
- Добавить logging для всех операций (debug level)
- Обрабатывать SQLAlchemyError и DatabaseError
