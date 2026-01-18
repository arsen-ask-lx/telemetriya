# Task: Virtual Environment Setup

## Goal
Создать Python виртуальное окружение, установить необходимые зависимости и инструменты разработки.

## Scope
### In Scope:
- Создание Python 3.11+ виртуального окружения (`.venv`)
- Установка production dependencies (`requirements.txt`)
- Установка development dependencies (`requirements-dev.txt`)
- Создание `pyproject.toml` с tool configs (pytest, ruff, mypy, coverage, isort)
- Проверка версий всех инструментов

### Out of Scope:
- Фактическая разработка кода (будет позже)
- Промпты и LLM интеграции (будут позже)

## Plan
1. Проверить версию Python: `python --version` (должна быть 3.11+)
2. Создать виртуальное окружение: `python -m venv .venv`
3. Активировать окружение:
   - Linux/Mac: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Создать `requirements.txt` с минимальными production зависимостями:
   ```
   fastapi>=0.104.0,<0.105.0
   uvicorn[standard]>=0.24.0,<0.25.0
   sqlalchemy[asyncio]>=2.0.0,<3.0.0
   asyncpg>=0.29.0,<0.30.0
   alembic>=1.12.0,<2.0.0
   pydantic>=2.5.0,<3.0.0
   pydantic-settings>=2.1.0,<3.0.0
   python-multipart>=0.0.6,<0.1.0
   python-jose[cryptography]>=3.3.0,<4.0.0
   passlib[bcrypt]>=1.7.4,<2.0.0
   python-dateutil>=2.8.2,<3.0.0
   httpx>=0.25.0,<0.26.0
   aiogram>=3.4.0,<4.0.0
   pypdf>=3.17.0,<4.0.0
   sentence-transformers>=2.2.0,<3.0.0
   ```
5. Создать `requirements-dev.txt` с dev зависимостями:
   ```
   -r requirements.txt
   pytest>=7.4.0,<8.0.0
   pytest-asyncio>=0.21.0,<1.0.0
   pytest-cov>=4.1.0,<5.0.0
   pytest-mock>=3.12.0,<4.0.0
   ruff>=0.1.0,<1.0.0
   mypy>=1.7.0,<2.0.0
   coverage>=7.3.0,<8.0.0
   types-python-dateutil>=2.8.0,<3.0.0
   types-passlib>=1.7.0,<2.0.0
   ```
6. Создать `pyproject.toml` с tool configs:
   ```toml
   [tool.ruff]
   line-length = 100
   target-version = "py311"
   select = ["E", "F", "I", "N", "W"]
   ignore = ["E501"]

   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = ["test_*.py"]
   python_classes = ["Test*"]
   python_functions = ["test_*"]
   asyncio_mode = "auto"

   [tool.mypy]
   python_version = "3.11"
   warn_return_any = true
   warn_unused_configs = true
   ignore_missing_imports = true

   [tool.coverage.run]
   source = ["src"]
   omit = ["tests/*", "*/__init__.py"]

   [tool.coverage.report]
   exclude_lines = [
       "pragma: no cover",
       "def __repr__",
       "raise AssertionError",
       "raise NotImplementedError",
   ]
   ```
7. Установить зависимости: `pip install -r requirements-dev.txt`
8. Проверить версии инструментов:
   - `python --version` (3.11+)
   - `pytest --version`
   - `ruff version`
   - `mypy --version`
   - `coverage --version`
9. Обновить `.gitignore` с `.venv/`
10. Commit: `git add . && git commit -m "chore: setup virtual environment and dependencies"`

## Files Allowlist
- `.venv/` (новая директория, но не коммитится в git)
- `requirements.txt` (новый файл)
- `requirements-dev.txt` (новый файл)
- `pyproject.toml` (новый файл)
- `.gitignore` (обновление)

## Definition of Done (DoD)
- [x] Виртуальное окружение `.venv/` создано
- [x] Python версия 3.11+
- [x] `requirements.txt` содержит production зависимости
- [x] `requirements-dev.txt` содержит dev зависимости
- [x] `pyproject.toml` содержит ruff, pytest, mypy, coverage конфиги
- [x] Все зависимости установлены (`pip list` показывает пакеты)
- [x] Инструменты работают:
  - `pytest --version` — показывает версию
  - `ruff version` — показывает версию
  - `mypy --version` — показывает версию
  - `coverage --version` — показывает версию
- [x] `.gitignore` содержит `.venv/`
- [x] Commit сделан

## Risks / Edge Cases
- **Python версия < 3.11:** нужно установить Python 3.11+ или использовать pyenv/conda
- **Windows line ending проблемы:** pip установки могут быть медленными
- **Virtual environment не активируется:** проверить скрипты в `.venv/Scripts/` или `.venv/bin/`
- **Conflict с глобальными пакетами:** всегда активировать venv перед установкой

## How to Verify
```bash
# Проверка Python версии (должна быть 3.11+)
python --version

# Проверка venv активации (путь должен содержать .venv)
which python  # Linux/Mac
where python  # Windows

# Проверка инструментов
pytest --version
ruff version
mypy --version
coverage --version

# Проверка зависимостей
pip list | grep -E "(fastapi|aiogram|pytest|ruff)"

# Проверка git
git status
git log --oneline -1
```

## Dependencies
- Task 001: Git & GitHub Setup (должен быть завершён)

## Estimated Time
1-2 часа

## Notes
- Всегда проверять что venv активирован (prompt должен содержать `(venv)`)
- Использовать `pip freeze > requirements.txt` для генерации, если нужно
- Версии в requirements.txt зафиксированы для стабильности
