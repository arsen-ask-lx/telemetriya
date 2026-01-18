# Project Structure Map (Flat View)
Описание архитектуры и назначения файлов проекта.

## 1. Конфигурация (Root)
* `AGENTS.md` — Глобальные правила (Конституция). Читается всеми агентами.
* `.gptignore` — Список исключений (аналог .gitignore для LLM).

## 2. Спецификации и Память (specs/)
**Docs (Общее)**
* `specs/docs/vision.md` — Исходное видение проекта (черновики идей).
* `specs/docs/plan.md` — Глобальный план развития проекта (Roadmap).

**Evals (Контроль качества)**
* `specs/evals/cases.jsonl` — "Золотой датасет". Примеры Input -> Expected Output.
* `specs/evals/run_eval.py` — Скрипт для автоматического прогона тестов.

**Memory (Контекст RCF)**
* `specs/memory/activeContext.md` — Оперативная память. Текущий статус задачи и фокус.
* `specs/memory/lessons.md` — Журнал ошибок и выводов (Learning Log).
* `specs/memory/structure.md` — ЭТОТ ФАЙЛ. Карта путей.

**Tasks (Рабочее пространство)**
* `specs/tasks/task-001-init` — ТЗ текущей задачи и критерии готовности (DoD).

## 3. Инструментарий агента (.opencode/)
* `.opencode/agents/breaker.md` — Промпт для роли Планировщика.
* `.opencode/agents/builder.md` — Промпт для роли Разработчика.
* `.opencode/agents/reviewer.md` — Промпт для роли Ревьюера.
* `.opencode/agents/archivist.md` — Промпт для роли Документатора.
