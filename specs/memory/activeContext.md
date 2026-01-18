# Active Context (оперативка)

> Source of Truth для текущего состояния. Обновляется после каждого task (или при смене фокуса).
> Держать коротким: 1 экран. Никаких обсуждений — только факты.

## Status
done (task-001, task-002, task-003 completed)

## Current Phase
- Phase: 0 - Infrastructure & Foundation (Дни 1-3)
- Tasks: 6 tasks created (001-006)
- Completed: task-001 (Git & GitHub), task-002 (Virtual Environment), task-003 (Project Structure)
- Estimated time: 3-4 days remaining

## Current Task
- Path: `specs/tasks/task-003-project-structure/task.md`
- Goal (1 sentence): Создать стандартную структуру директорий проекта и __init__.py файлы.
- Status: DONE (reviewer APPROVED)

## Scope (what we do now)
- Phase 0: Infrastructure & Foundation:
  - Git & GitHub Setup (task-001)
  - Virtual Environment Setup (task-002)
  - Project Structure Setup (task-003)
  - Configuration Management (task-004)
  - Logging Setup (task-005)
  - GitHub Actions CI/CD (task-006)

## Out of Scope (not now)
- Реализация бота, API, БД (Phase 1+)
- AI интеграции (Phase 5+)
- Deployment (Phase 9)

## Next Steps (max 3)
1) Execute task-004-config-management (owner to start)
2) Execute task-005-logging-setup
3) Execute task-006-github-actions-cicd

## Blockers
None

## Decisions (only if important)
- Stack: Python 3.11+, FastAPI, PostgreSQL + pgvector, LLM (glm-4.7/ollama/gemini)
- Methodology: TDD (Red → Green → Refactor), Progressive Complexity
- GitHub: https://github.com/arsen-ask-lx/telemetriya.git

## Done Criteria for Phase 0
- [x] Git репозиторий инициализирован и подключен к GitHub
- [x] Виртуальное окружение с зависимостями создано
- [x] Структура проекта создана
- [ ] Конфигурация с Pydantic Settings работает
- [ ] Логирование с PII masking работает
- [ ] GitHub Actions CI/CD pipeline работает
- [ ] Все задачи (001-006) выполнены и протестированы
- [ ] CI/CD passes на main branch

## Last Updated
- Date: 2026-01-18
- By: archivist

## What was done
- Task-001-git-github-setup: Git repo initialized, GitHub connected, base docs created (README, LICENSE, CONTRIBUTING, CHANGELOG, .gitignore, .gitattributes)
- Task-002-virtual-env-setup: Python 3.12.10 venv created, all dependencies installed (production + dev), tool configs created (pyproject.toml with ruff, pytest, mypy, coverage)
- Task-003-project-structure: Full project structure created (src/, tests/, storage/, scripts/, infra/, docs/), 26 __init__.py files, 9 .gitkeep files, .env.example template, .gitignore updated (commit 21c9d46)
- All verification checks passed for task-001, task-002, task-003
- Initial task-003 review failed due to .gitkeep files not tracked (gitignore issues), fixed on second attempt
- Commit amended (d4351aa → 21c9d46) to include all .gitkeep files
