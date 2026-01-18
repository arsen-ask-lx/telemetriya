# Project Structure Map (Flat View)
Описание архитектуры и назначения файлов проекта.

## 1. Конфигурация (Root)
* `AGENTS.md` — Глобальные правила (Конституция). Читается всеми агентами.
* `.gptignore` — Список исключений (аналог .gitignore для LLM).
* `.gitignore` — Git исключения (Python, secrets, cache, venv, node_modules, *.db).
* `.gitattributes` — Git настройки (line endings LF, LFS для больших файлов).
* `README.md` — Документация проекта (описание, установка, запуск).
* `LICENSE` — MIT лицензия.
* `CONTRIBUTING.md` — Правила контрибьюции (Conventional Commits, TDD, Code of Conduct).
* `CHANGELOG.md` — Журнал изменений (Keep a Changelog format).

## 2. Спецификации и Память (specs/)
**Docs (Общее)**
* `specs/docs/vision.md` — Исходное видение проекта (черновики идей).
* `specs/docs/plan.md` — Глобальный план развития проекта (Roadmap).

**Evals (Контроль качества)**
* `specs/evals/cases.jsonl` — "Золотой датасет". Примеры Input -> Expected Output.
* `specs/evals/run_eval.py` — Скрипт для автоматического прогона тестов.
* `specs/evals/verify_git_setup.py` — Проверочный скрипт для task-001 (TDD RED phase).
* `specs/evals/verify_venv_setup.py` — Проверочный скрипт для task-002 (создан builder).

**Memory (Контекст RCF)**
* `specs/memory/activeContext.md` — Оперативная память. Текущий статус задачи и фокус.
* `specs/memory/lessons.md` — Журнал ошибок и выводов (Learning Log).
* `specs/memory/structure.md` — ЭТОТ ФАЙЛ. Карта путей.

**Tasks (Рабочее пространство)**
* `specs/tasks/task-001-git-github-setup/task.md` — Task-001 (COMPLETED): Git & GitHub Setup.
* `specs/tasks/task-002-virtual-env-setup/task.md` — Task-002 (NEXT): Virtual Environment Setup.
* `specs/tasks/task-003-project-structure/task.md` — Task-003: Project Structure Setup.
* `specs/tasks/task-004-config-management/task.md` — Task-004: Configuration Management.
* `specs/tasks/task-005-logging-setup/task.md` — Task-005: Logging Setup.
* `specs/tasks/task-006-github-actions-cicd/task.md` — Task-006: GitHub Actions CI/CD.

## 3. Инструментарий агента (.opencode/)
* `.opencode/agents/breaker.md` — Промпт для роли Планировщика.
* `.opencode/agents/builder.md` — Промпт для роли Разработчика.
* `.opencode/agents/reviewer.md` — Промпт для роли Ревьюера.
* `.opencode/agents/archivist.md` — Промпт для роли Документатора.
