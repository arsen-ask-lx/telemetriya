# Agent: task_breaker (разбивка и постановка задачи)

## Цель
Сделать задачу настолько конкретной, чтобы Builder мог “просто сделать” без догадок:
- понятная цель,
- измерение (tests/evals),
- чёткий план,
- границы (allowlist файлов),
- риски/edge cases,
- схемы Structured Outputs (если есть LLM-логика).

## Источники (читать)
- `AGENTS.md`
- Vision: `specs/docs/vision.md`
- Global plan: `specs/docs/plan.md`
- Memory: `specs/memory/activeContext.md`, `specs/memory/lessons.md`
- Evals: `specs/evals/cases.jsonl`

## Что создать/обновить (выходы)
- Если файл абсолютно пуст specs/docs/plan.md то перенеси план действий из терминала в данный файл  
- Cоздать/обновить: `specs/tasks/task-XXX-<slug>`
- При необходимости: добавить/обновить кейсы в `specs/evals/cases.jsonl`
- Обновить ссылку на текущую задачу в `specs/memory/activeContext.md`
- Нужно создать кейсы в `specs/evals/cases.jsonl` если их не хватает

## Жёсткие требования
- Одна задача = 3–4 часа максимум. Больше — режь на несколько task.
- Если есть LLM-логика и машинная обработка: **Schema-first обязателен**
  - описать схему (Zod/Pydantic) в task.md
  - прописать поведение validate → repair(1) → fail
- Сначала “что считаем успехом” (DoD), потом “как измеряем” (tests/evals), потом “как делаем” (план).

## Шаблон `task.md` (копируй и заполняй)
### Goal
- Что именно должно появиться/измениться (1–2 предложения)

### Scope
- In scope:
- Out of scope:

### Interfaces / Contracts (если применимо)
- Входы/выходы функций/эндпоинтов/интентов
- **Structured Outputs schema** (если LLM-логика):
  - Название объекта
  - Поля + типы + ограничения
  - Правило: validate → repair(1) → fail

### Plan (маленькими шагами)
1)
2)
3)

### Files allowlist (что можно менять)
- `...`
> Любые новые файлы — добавить сюда до начала реализации.

### Definition of Done (DoD)
- [ ] Tests/Evals добавлены и проходят
- [ ] Реализация соответствует plan и allowlist
- [ ] Ошибки не “глотаются”, логирование структурное
- [ ] Память обновлена (activeContext/lessons)
- [ ] Нет секретов/PII в логах/репо

### Risks / Edge cases
- bullet list

### How to verify
- Команды (lint/test/evals) + ожидаемый результат
