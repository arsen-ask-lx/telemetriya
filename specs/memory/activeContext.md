# Active Context (оперативка)

> Source of Truth для текущего состояния. Обновляется после каждого task (или при смене фокуса).
> Держать коротким: 1 экран. Никаких обсуждений — только факты.

## Status
planning | building | review | done

## Current Phase
- Phase: 0 - Infrastructure & Foundation (Дни 1-3)
- Tasks: 6 tasks created (001-006)
- Estimated time: 4-5 days

## Current Task
- Path: `specs/tasks/task-001-git-github-setup/task.md`
- Goal (1 sentence): Настроить Git репозиторий, подключить к GitHub и создать базовую документацию.
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
1) Execute task-001-git-github-setup
2) Execute task-002-virtual-env-setup
3) Execute task-003-project-structure

## Decisions (only if important)
- Stack: Python 3.11+, FastAPI, PostgreSQL + pgvector, LLM (glm-4.7/ollama/gemini)
- Methodology: TDD (Red → Green → Refactor), Progressive Complexity
- GitHub: https://github.com/arsen-ask-lx/telemetriya.git

## Done Criteria for Phase 0
- [ ] Git репозиторий инициализирован и подключен к GitHub
- [ ] Виртуальное окружение с зависимостями создано
- [ ] Структура проекта создана
- [ ] Конфигурация с Pydantic Settings работает
- [ ] Логирование с PII masking работает
- [ ] GitHub Actions CI/CD pipeline работает
- [ ] Все задачи (001-006) выполнены и протестированы
- [ ] CI/CD passes на main branch

## Last Updated
- Date: 2026-01-18
- By: task_breaker
