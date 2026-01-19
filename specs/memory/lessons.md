# Lessons Learned (what went wrong/right)

## 2026-01-19 (Task-008: SQLAlchemy Models & Base Classes)
**What went well:**
- Base declarative class created successfully using DeclarativeBase (SQLAlchemy 2.0)
- 3 mixins implemented correctly: TimestampMixin, UUIDMixin, SoftDeleteMixin
- 5 models created with full type hints: User, Note, Reminder, TodoistTask, Session
- All enums defined properly: ContentType, NoteSource, SyncStatus
- Indexes created for frequently queried fields (composite indexes where needed)
- 54 unit tests created with 100% coverage (90 statements, 0 missed)
- mypy validation passed (no issues found in 10 source files)
- ruff linting passed after automatic fixes (sorted imports, removed unused)
- Foreign key cascades configured correctly (CASCADE for user_id, SET NULL for note_id)
- JSON workaround documented for vector_embedding (pgvector pending in dev)

**What went wrong:**
- Initial attempt used `MappedAsDataclass` in Base → SQLAlchemy dataclass error with mixins
  - Error: "non-default argument 'deleted_at' follows default argument"
  - Fix: Removed `MappedAsDataclass`, used plain `DeclarativeBase`
- SQLAlchemy reserved word `metadata` caused error
  - Error: "Attribute name 'metadata' is reserved when using Declarative API"
  - Fix: Renamed to `note_metadata` in Python, kept `"metadata"` as column name in DB
- Some lint issues existed initially (unsorted imports, unused imports: Index, ARRAY, BigInteger)
  - Fix: Ran `ruff check --fix` to auto-fix all issues

**What was fixed:**
- Changed Base from `DeclarativeBase, MappedAsDataclass` to `DeclarativeBase` only
- Renamed `metadata` field to `note_metadata` in Note model (DB column stays "metadata")
- Fixed all lint issues with `ruff check --fix src/db/`

**What could be improved:**
- SAWarning in tests when reusing `TestModel` class name for different mixin tests
  - Could use unique names like `TimestampTestModel`, `UUIDTestModel`
- Pydantic schemas not created (optional in task scope, not in DoD)
  - If needed for FastAPI, should be separate task
- Vector embedding using JSON as temporary workaround
  - Should migrate to `pgvector.Vector(1536)` when extension is available

**Lessons:**
1. **SQLAlchemy 2.0 and mixins:**
   - `MappedAsDataclass` in Base conflicts with mixins containing default vs non-default fields
   - Use plain `DeclarativeBase` unless dataclass features are explicitly needed
   - If using mixins, ensure all fields either all have defaults or are all required

2. **SQLAlchemy reserved names:**
   - `metadata` is a reserved attribute in SQLAlchemy declarative models
   - Workaround: Rename Python attribute (e.g., `note_metadata`) and specify column name: `mapped_column("metadata", ...)`

3. **pgvector workaround:**
   - If pgvector extension not installed in dev environment, use JSON for vector embeddings
   - Document as temporary workaround, create follow-up task for migration to `pgvector.Vector`

4. **Composite indexes in SQLAlchemy:**
   - Use `__table_args__ = (Index("idx_name", "col1", "col2"),)` for multi-column indexes
   - Single-column indexes can use `mapped_column(..., index=True)`

5. **Foreign key cascades:**
   - CASCADE for user_id: delete user → delete related records
   - SET NULL for optional note_id: delete note → set note_id to NULL
   - Document cascade decisions in model docstrings

6. **Test warnings for class reuse:**
   - SAWarning occurs when same class name is used multiple times in test files
   - Acceptable for unit tests but can be confusing in logs

---

## 2026-01-18 (Task-006: GitHub Actions CI/CD)
**What went well:**
- GitHub Actions CI/CD workflow created successfully (.github/workflows/ci.yml)
- 3 jobs configured (lint, typecheck, test) with pip caching
- All checks pass locally after fixes: lint (All checks passed!), typecheck (Success: no issues found), tests (27 passed, 97% coverage)
- Python version synchronized: pyproject.toml (3.12) = CI workflow (3.12) = local venv (3.12.10)
- Reviewer APPROVED after all critical fixes

**What went wrong:**
- Python version mismatch: CI workflow used Python 3.11 but pyproject.toml configured for 3.12
- Initial implementation didn't verify Python version consistency across CI, pyproject.toml, and venv
- 26 lint errors existed in code from previous tasks (unsorted imports, unused imports)
- pyproject.toml had deprecated ruff configuration (top-level instead of [tool.ruff.lint])
- test_prod_mode_uses_pii_formatter failed due to missing re-import after module reload
- pydantic/pydantic-core incompatibility after venv recreation

**What was fixed:**
- Updated .github/workflows/ci.yml: python-version 3.11 -> 3.12 (3 places: lines 18, 48, 78)
- Fixed 26 lint errors with `ruff check . --fix` (sorted imports, removed unused imports)
- Updated pyproject.toml: added [tool.ruff.lint] section (fixed deprecation warning)
- Fixed test_prod_mode_uses_pii_formatter: re-import PIIFormatter after module reload
- Recreated venv with Python 3.12.10
- Force reinstalled pydantic/pydantic-core for Python 3.12 compatibility

**What could be improved:**
- Builder should verify Python version consistency across CI, pyproject.toml, and local venv before commit
- Lint should be run automatically as part of pre-commit hooks to catch errors earlier
- Task-006 allowlist was too narrow (excluded files with lint errors that needed fixing)
- Consider adding automated lint/typecheck checks before pushing (pre-commit)

**Lessons:**
- Python version consistency is critical: CI workflow = pyproject.toml = local venv
- datetime.UTC requires Python 3.11+, ensure Python version matches code requirements
- ruff check . --fix can fix most lint issues automatically, but run it before committing
- pyproject.toml ruff configuration should use [tool.ruff.lint] section (new format in ruff 0.14+)
- When reloading Python modules in tests, re-import symbols that were deleted from sys.modules
- pydantic/pydantic-core must be reinstalled when switching Python versions
- CI pipeline verification: test locally with act or run all checks manually before pushing
- Lint errors accumulate quickly; run lint regularly to keep codebase clean

---

## 2026-01-18 (Task-005: Logging Setup)
**What went well:**
- PIIFormatter successfully masks emails, tokens, and phone numbers
- TextFormatter with ANSI colors works correctly for dev mode
- Unicode support (Russian language) implemented via ensure_ascii=False in json.dumps()
- 17 unit tests created, 100% pass rate
- Coverage 94% (above required 80%)
- Type hints validated with mypy (no issues)
- Reviewer APPROVED without changes

**What went right:**
- Fixed datetime.utcnow() deprecation warning by using datetime.now(UTC)
- Correctly typed formatter union: `formatter: logging.Formatter`
- All PII patterns tested (emails, tokens, phones, multiple PII in one message)
- False positive prevention: short alphanumeric strings (<20 chars) NOT masked as tokens

**What could be improved:**
- Optional log rotation handler not implemented (noted as optional in task, could be added later)
- ANSI colors on legacy Windows terminals might require colorama (edge case)

**Lessons:**
- datetime.utcnow() is deprecated in Python 3.12+, use datetime.now(UTC) instead
- For Formatter type hints: use `formatter: logging.Formatter` as base type for Union
- ensure_ascii=False in json.dumps() for proper Unicode support (Russian, etc.)
- Regex patterns for PII: test thoroughly for both positives and false positives
- Coverage 94% for logging module is excellent (3 missing lines: edge cases)
- Dev/prod mode switching works correctly via DEBUG environment variable
- Context injection (extra context) is captured automatically by extracting non-standard LogRecord fields

---

## 2026-01-18 (Task-007: Docker + PostgreSQL 16 with pgvector)
**What went well:**
- Docker Compose создан успешно с PostgreSQL 16 + pgvector image
- pgvector extension установлен корректно (vector 0.8.1 + uuid-ossp)
- Health checks работают (pg_isready, interval 10s, timeout 5s, retries 5)
- Persistent volumes настроены (postgres-data volume)
- Network isolation создана (telemetriya-network bridge)
- Cross-platform скрипты созданы (8 скриптов: 4 .sh для Unix + 4 .bat для Windows)
- 11 unit тестов созданы и проходят (docker-compose validation + scripts existence)
- Контейнеры успешно запускаются и останавливаются
- Данные переживают перезапуск (test_persistence таблица сохранялась)
- psql подключение работает через скрипты
- README.md обновлён с подробными инструкциями по Docker и управлению
- .env.example обновлён с POSTGRES_* переменными
- Reviewer APPROVED без блокирующих изменений
- Все проверки DoD выполнены

**What went wrong:**
- Первоначальный volume mount для init.sql был неправильный: `./infra/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql`
- Docker видел `init.sql` как директорию (файл с таким же именем существовал: infra/postgres/.gitkeep)
- Логи показывали: "error: could not read from input file: Is a directory"
- pgvector extension не устанавливался на первом запуске (инициализация пропускалась из-за ошибки)
- Требовалась ручная проверка Docker чтобы найти причину проблемы

**What was fixed:**
- Изменён volume mount: `${PWD}/infra/postgres/init.sql:/docker-entrypoint-initdb.d/00-init.sql:ro`
- Добавлен `${PWD}` для абсолютного пути (работает на Windows/Linux/Mac)
- Переименован файл mount в `00-init.sql` чтобы избежать конфликта с директорией
- Добавлен флаг `:ro` (read-only) для безопасности init скриптов
- После исправления: pgvector и uuid-ossp успешно установлены
- Persistent volumes подтверждены (данные переживают перезапуск)
- Контейнер проходит health checks (статус "healthy")

**What could be improved:**
- Для тестов docker-compose использовался `pyyaml==6.0.2` без явного разрешения в task.md allowlist
- Логично и необходимо для работы тестов, но лучше добавить в allowlist будущих Docker-задач
- Ручная проверка Docker контейнеров (запуск, остановка, подключение psql) полезна, но не автоматизирована
- Persistence volumes тестирование: можно добавить интеграционный тест, который создаёт таблицу, останавливает контейнер, запускает снова и проверяет что данные есть
- Для интеграционного теста потребуются Docker Python SDK или subprocess для управления контейнерами из Python кода
- Windows скрипты `.bat` работают, но можно улучшить error handling (проверка кода завершения)
- Тесты для скриптов проверяют только существование, можно добавить тесты правильности команд

**Lessons:**
1. **Volume mounts с относительными путями** — Docker может интерпретировать файл как директорию, если есть конфликт имён. Решение: использовать `${PWD}` или абсолютные пути, переименовать файлы чтобы избежать конфликтов.
2. **`:ro` флаг для read-only** — init скрипты должны быть смонтированы только для чтения для безопасности.
3. **Чтение логов Docker** — при отладке проблем с Docker, всегда проверять `docker-compose logs postgres` и искать специфические ошибки.
4. **Ручная верификация Docker** — после создания инфраструктуры всегда запускать и проверять вручную:
   - `docker-compose ps` (статус контейнеров)
   - `docker-compose logs` (логи на ошибки)
   - Подключение к БД для проверки расширений
5. **Health checks критически важны** — проверять что контейнер переходит в статус "healthy" после запуска.
6. **Persistent volumes тестирование** — создавать тестовую таблицу, останавливать контейнер, запускать снова и проверять что данные есть. Это подтверждает что volumes работают корректно.
7. **Кроссплатформенные скрипты** — создавать версии для Unix (.sh) и Windows (.bat), использовать только команды которые работают на обеих платформах.
8. **${PWD} переменная** — Docker Compose использует `${PWD}` для текущей директории, это работает на всех системах (Windows/Linux/Mac).
9. **pgvector/pgvector:pg16 image** — использовать официальный образ с pgvector вместо базового postgres + ручной установки extensions. Это проще и надёжнее.
10. **Naming init скриптов** — использовать числовые префиксы (00-init.sql, 01-custom.sql) чтобы избежать конфликтов с директориями в docker-entrypoint-initdb.d/.

---

## 2026-01-18 (Task-001: Git & GitHub Setup)
**What went well:**
- TDD approach applied successfully (RED → GREEN → REFINEMENT)
- Created verification script `verify_git_setup.py` for all DoD checks
- All checks passed (10/10, 100%)
- Documentation quality: well-structured README, LICENSE, CONTRIBUTING, CHANGELOG

**What could be improved:**
- Verification scripts should be included in task allowlist (currently not specified)
- Builder agent tried to start task-002 before task-001 was fully reviewed → added constraint: one task per session

**Lessons:**
- Always create verification scripts before implementation (TDD approach)
- Add verification scripts to task allowlist explicitly
- Update agent constraints to prevent task jumping
- Git line ending issues on Windows: solved with .gitattributes (LF normalization)

## 2026-01-18 (Task-002: Virtual Environment Setup)
**What went well:**
- Python 3.12.10 successfully found and used for venv
- All dependencies installed correctly (production + dev)
- Tool configs created properly (ruff, pytest, mypy, coverage in pyproject.toml)
- Issue caught by reviewer and fixed promptly

**What went wrong:**
- Initial venv created with Python 3.10.11 instead of 3.11+ (DoD requirement)
- Builder didn't check Python version before creating venv → first review returned CHANGES_REQUESTED
- pyproject.toml initially configured for py311, had to update to py312 after venv recreation

**What could be improved:**
- Builder should verify Python version explicitly before creating venv (Step 1 of task plan)
- Add Python version check to verification commands in task DoD

**Lessons:**
- Always verify Python version matches DoD requirements before creating venv
- Sync pyproject.toml python_version with actual venv Python version
- Document fixes properly in commit messages (e.g., "fix: recreate venv with Python 3.12.10 (DoD requires 3.11+)")

## 2026-01-18 (Task-003: Project Structure Setup)
**What went well:**
- Full project structure created correctly (37 directories)
- All 26 __init__.py files created
- All 9 .gitkeep files created and committed
- .env.example template created with all required sections
- Python imports verified working

**What went wrong:**
- Initial commit (d4351aa) failed review because .gitkeep files were not tracked by git
- Issue: .gitignore rules `secrets/` and `temp/` blocked files even with exceptions `!infra/secrets/.gitkeep` and `!storage/temp/.gitkeep`
- Builder didn't verify that .gitkeep files were actually in git commit

**What was fixed:**
- Removed broad rule `secrets/` (was blocking infra/secrets/.gitkeep)
- Changed `temp/` to `/temp` (only root temp directory)
- Changed `storage/` to `storage/*` with proper exceptions
- Added exceptions: `!storage/pdf/`, `!storage/voice/`, `!storage/temp/`
- Added `!storage/temp/.gitkeep` before `/temp` rule (order matters in .gitignore)
- Re-added all .gitkeep files to git and amended commit (d4351aa → 21c9d46)

**What could be improved:**
- Builder should verify that .gitkeep files are actually tracked by git before committing
- Add explicit check: `git check-ignore <file>` to verify exclusions work
- Add verification of git commit contents: `git show --name-only HEAD | grep gitkeep`

**Lessons:**
- Order matters in .gitignore: exclusions (!) should come before broader rules that block them
- Broad directory rules like `secrets/` block subdirectories even with exclusions
- Use `/*` for directory contents while allowing specific files via exclusions
- Always verify .gitkeep files are tracked: `git ls-tree -r HEAD | grep gitkeep`
- Amended commits change hash - important to know if not yet pushed
- Use `git check-ignore -v <file>` to debug .gitignore issues

## 2026-01-18 (Task-004: Configuration Management)
**What went well:**
- Pydantic Settings v2 implementation successful with all config fields
- @lru_cache for singleton get_settings() implemented correctly
- All environment variables supported via validation_alias
- 10 unit tests created, initial coverage 100%
- mypy passed without errors
- Reviewer feedback addressed promptly

**What went wrong:**
- Initial implementation didn't include SECRET_KEY validation (identified as risk in task.md)
- Tests were not isolated from local .env file → reviewer CHANGES_REQUESTED
  - Pydantic Settings loads .env automatically even when using patch.dict(os.environ, ..., clear=True)
  - Tests would fail if .env existed locally with different values
- Initial review returned CHANGES_REQUESTED with 2 critical findings
  - Required fix: isolate_from_env_file fixture
  - Required fix: SECRET_KEY validation (min 16 chars)
  - Required fix: update all SECRET_KEY values in tests to be >=16 chars

**What was fixed:**
- Added `@field_validator("secret_key")` to validate minimum length (16 chars)
- Added `isolate_from_env_file()` fixture with autouse=True:
  - Temporarily renames .env → .env.backup before tests
  - Restores .env.backup → .env after tests (in finally block)
- Added `test_settings_secret_key_min_length` test
- Updated all SECRET_KEY values in tests to be >=16 chars
- Fixed fixture error (removed duplicate yield in isolate_from_env_file)
- Updated .env.example with SECRET_KEY min length comment

**What could be improved:**
- Builder should anticipate that Pydantic Settings loads .env file automatically
- Test isolation fixtures should be added proactively for any environment-dependent code
- Validation for critical fields (SECRET_KEY, tokens) should be implemented in initial implementation, not as a follow-up

**Lessons:**
- Pydantic Settings loads .env file automatically via model_config, even with os.environ patching
- For test isolation from .env: temporarily rename .env or use _env_file=None parameter
- Validation of security-critical fields (SECRET_KEY, API tokens) should be implemented from the start
- Test fixtures for environment isolation are essential for deterministic test results
- Review cycle: initial implementation → CHANGES_REQUESTED → fixes → APPROVED is normal workflow
