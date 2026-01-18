# Task: GitHub Actions CI/CD

## Goal
Настроить автоматизированный CI/CD pipeline с GitHub Actions для проверки качества кода (lint, typecheck, tests).

## Scope
### In Scope:
- Создание `.github/workflows/ci.yml` для continuous integration
- Lint checks (ruff)
- Type checks (mypy)
- Unit tests (pytest)
- Coverage reporting (pytest-cov)
- Upload coverage to Codecov (опционально)
- Настройка required checks для merge
- Настройка branch protection rules (в GitHub UI, не через файл)

### Out of Scope:
- Deployment pipeline (будет позже в Фазе 9)
- E2E tests (будут позже)
- Integration tests (будут позже)
- Automatic tagging (будет позже)

## Plan (TDD: Red → Green → Refactor)

### Phase 1: Red (Tests — Conceptual)
1. Нет unit тестов для CI/CD workflow (workflow не является Python кодом)
2. Вместо этого: определить что CI должно проверять (definition of done)

### Phase 2: Green (Implementation)
3. Создать `.github/workflows/ci.yml`:
   ```yaml
   name: CI

   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main, develop ]

   jobs:
     lint:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             python -m venv .venv
             source .venv/bin/activate
             pip install --upgrade pip
             pip install ruff

         - name: Run ruff
           run: |
             source .venv/bin/activate
             ruff check .

     typecheck:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             python -m venv .venv
             source .venv/bin/activate
             pip install --upgrade pip
             pip install -r requirements-dev.txt

         - name: Run mypy
           run: |
             source .venv/bin/activate
             mypy src/

     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             python -m venv .venv
             source .venv/bin/activate
             pip install --upgrade pip
             pip install -r requirements-dev.txt

         - name: Run tests
           run: |
             source .venv/bin/activate
             pytest --cov=src --cov-report=xml --cov-report=term-missing

         - name: Upload coverage reports to Codecov
           uses: codecov/codecov-action@v3
           if: success()
           with:
             files: ./coverage.xml
             flags: unittests
             name: codecov-umbrella
           env:
             CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
   ```
4. Создать `.github/workflows/` директорию если не существует
5. Commit: `git add .github/ && git commit -m "ci: add GitHub Actions workflow for lint/typecheck/tests"`

### Phase 3: Refactor
6. Оптимизировать workflow (кэширование pip, параллельное выполнение):
   ```yaml
     # Добавить caching
     - name: Cache pip packages
       uses: actions/cache@v3
       with:
         path: ~/.cache/pip
         key: ${{ runner.os }}-pip-${{ hashFiles('requirements-dev.txt') }}
         restore-keys: |
           ${{ runner.os }}-pip-

     # Оптимизировать параллельное выполнение (jobs уже параллельны по умолчанию)
   ```
7. Добавить GitHub secret для Codecov (опционально):
   - GitHub Repository → Settings → Secrets and variables → Actions → New repository secret
   - Name: `CODECOV_TOKEN`
   - Value: (получить с https://codecov.io)

### Phase 4: Integration (GitHub UI)
8. Настроить branch protection rules:
   - GitHub Repository → Settings → Branches → Add rule
   - Rule name: `main`
   - Settings:
     - ✅ Require a pull request before merging
     - ✅ Require approvals (1 approval)
     - ✅ Require status checks to pass before merging
       - ✅ Require branches to be up to date before merging
       - ✅ Lint (from ci.yml)
       - ✅ Typecheck (from ci.yml)
       - ✅ Test (from ci.yml)
9. Настроить required checks:
   - GitHub Repository → Settings → Branches → main → Require status checks to pass
   - Добавить: `lint`, `typecheck`, `test`

### Phase 5: Verification
10. Создать pull request для тестирования CI
11. Проверить что все проверки (lint, typecheck, test) запускаются
12. Merge pull request если все проверки зелёные

## Files Allowlist
- `.github/workflows/ci.yml` (новый файл)
- `.github/workflows/` (новая директория)

## Definition of Done (DoD)
- [x] `.github/workflows/ci.yml` создан с 3 jobs: lint, typecheck, test
- [x] Lint check использует `ruff check .`
- [x] Typecheck использует `mypy src/`
- [x] Test использует `pytest --cov=src`
- [x] Coverage загружается на Codecov (опционально)
- [x] CI запускается на push/PR к main/develop
- [x] Branch protection rules настроены в GitHub UI
- [x] Required checks настроены: lint, typecheck, test
- [x] Workflow работает (можно увидеть в Actions tab на GitHub)
- [x] Commit сделан

## Risks / Edge Cases
- **Secrets management:** CODECOV_TOKEN должен быть настроен в GitHub secrets
- **False positives в lint/typecheck:** могут блокировать merge без причины
- **Slow tests:** CI может быть медленным если тестов много (оптимизировать позже)
- **GitHub Actions limits:** free tier имеет ограничения по времени (2000 минут/месяц)

## How to Verify
```bash
# Локально тестировать CI (опционально, с act)
# brew install act  # Mac
# act -v

# Проверить workflow файл
cat .github/workflows/ci.yml

# Push для триггера CI
git add .github/workflows/ci.yml
git commit -m "ci: add workflow"
git push origin feature/ci

# Открыть https://github.com/arsen-ask-lx/telemetriya/actions
# Убедиться что workflow запустился

# Создать PR и проверить что checks запускаются
```

## Dependencies
- Task 001: Git & GitHub Setup (должен быть завершён)
- Task 002: Virtual Environment Setup (должен быть завершён)
- Task 003: Project Structure Setup (должен быть завершён)
- Task 004: Configuration Management (должен быть завершён)
- Task 005: Logging Setup (должен быть завершён)

## Estimated Time
4-5 часов

## Notes
- GitHub Actions — это SaaS CI/CD, работает без локальной настройки
- Branch protection rules настраиваются в GitHub UI, не через файлы
- Required checks — это CI checks которые должны быть зелёными для merge
- Codecov не обязателен, но полезен для tracking coverage over time
- Actions cache (pip) ускоряет subsequent runs
- Для разработки можно использовать `act` для локального тестирования workflows
