# Task: Git & GitHub Setup

## Goal
Настроить Git репозиторий, подключить к GitHub и создать базовую документацию проекта.

## Scope
### In Scope:
- Инициализация локального Git репозитория
- Подключение к GitHub remote
- Создание `.gitignore` (Python, secrets, cache, .env, *.db, node_modules)
- Создание `.gitattributes` (line endings, LFS для больших файлов)
- Создание `README.md` с базовыми инструкциями
- Создание `LICENSE` (MIT)
- Создание `CONTRIBUTING.md` (конвенции коммитов, Code of Conduct)
- Создание `CHANGELOG.md` (формат версионирования)
- First commit и push на GitHub

### Out of Scope:
- GitHub Actions (будет в task-006-ci-cd)
- Документация API/архитектуры (будет позже)
- Licensing complexity (простая MIT)

## Plan
1. Инициализировать локальный Git репозиторий: `git init`
2. Создать `.gitignore` с правильными исключениями (Python, secrets, cache, .env, *.db, node_modules)
3. Создать `.gitattributes` для настройки line endings и LFS
4. Добавить GitHub remote: `git remote add origin https://github.com/arsen-ask-lx/telemetriya.git`
5. Создать `README.md` с:
   - Описание проекта
   - Краткое видение
   - Инструкция по установке (пока placeholder, так как пока нет зависимостей)
   - Инструкция по запуску (пока placeholder)
6. Создать `LICENSE` (MIT)
7. Создать `CONTRIBUTING.md` с:
   - Conventional Commits формат
   - Code of Conduct
   - Процесс разработки (TDD, review)
8. Создать `CHANGELOG.md` с форматом (Keep a Changelog)
9. Сделать first commit: `git add . && git commit -m "feat: initial project setup"`
10. Создать ветку main: `git branch -M main`
11. Push на GitHub: `git push -u origin main`

## Files Allowlist
- `.gitignore` (новый файл)
- `.gitattributes` (новый файл)
- `README.md` (новый файл)
- `LICENSE` (новый файл)
- `CONTRIBUTING.md` (новый файл)
- `CHANGELOG.md` (новый файл)
- `specs/docs/vision.md` (чтение для README)

## Definition of Done (DoD)
- [x] Git репозиторий инициализирован (`git status` работает)
- [x] GitHub remote добавлен (`git remote -v` показывает origin)
- [x] `.gitignore` исключает: __pycache__, *.pyc, .env, .venv, node_modules, *.db, secrets
- [x] `.gitattributes` настраивает line endings (LF) и LFS для больших файлов
- [x] `README.md` содержит описание проекта и placeholder инструкции
- [x] `LICENSE` файл создан (MIT)
- [x] `CONTRIBUTING.md` содержит Conventional Commits формат и Code of Conduct
- [x] `CHANGELOG.md` содержит формат версионирования
- [x] First commit сделан (`git log` показывает 1 коммит)
- [x] Push на GitHub успешный (репозиторий доступен на https://github.com/arsen-ask-lx/telemetriya)

## Risks / Edge Cases
- **GitHub репозиторий уже существует:** нужно проверить и удалить/синхронизировать
- **Line ending проблемы:** Windows/CRLF vs Linux/LF — решить через .gitattributes
- **LFS для больших файлов:** решить нужно ли LFS (PDF, аудио) или исключить из репозитория

## How to Verify
```bash
# Проверка Git
git status
git remote -v
git log --oneline

# Проверка файлов exist
ls -la .gitignore .gitattributes README.md LICENSE CONTRIBUTING.md CHANGELOG.md

# Проверка GitHub
# Открыть https://github.com/arsen-ask-lx/telemetriya в браузере
# Убедиться что все файлы видны
```

## Dependencies
Нет (первая задача)

## Estimated Time
2-3 часа

## Notes
- Использовать MIT лицензию (простая и пермиссивная)
- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Keep a Changelog формат для CHANGELOG.md
