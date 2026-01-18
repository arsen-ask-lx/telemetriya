# Active Context (оперативка)

> Source of Truth для текущего состояния. Обновляется после каждого task (или при смене фокуса).
> Держать коротким: 1 экран. Никаких обсуждений — только факты.

## Status
done (task-001 completed)

## Current Phase
- Phase: 0 - Infrastructure & Foundation (Дни 1-3)
- Tasks: 6 tasks created (001-006)
- Estimated time: 4-5 days

## Current Task
- Path: `specs/tasks/task-002-virtual-env-setup/task.md`
- Goal (1 sentence): Создать Python виртуальное окружение, установить зависимости и инструменты разработки.
- Status: Ready to implement

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
1) Execute task-002-virtual-env-setup
2) Execute task-003-project-structure
3) Execute task-004-config-management

## Decisions (only if important)
- Stack: Python 3.11+, FastAPI, PostgreSQL + pgvector, LLM (glm-4.7/ollama/gemini)
- Methodology: TDD (Red → Green → Refactor), Progressive Complexity
- GitHub: https://github.com/arsen-ask-lx/telemetriya.git

## Done Criteria for Phase 0
- [x] Git репозиторий инициализирован и подключен к GitHub
- [ ] Виртуальное окружение с зависимостями создано
- [ ] Структура проекта создана
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
- All 10 verification checks passed (100% pass-rate)
- Agent constraints updated (builder limited to one task per session)
