# Task: Logging Setup

## Goal
Реализовать robust logging system с structured logging (JSON для prod, text для dev), PII masking и log rotation.

## Scope
### In Scope:
- Создание `src/core/logging.py` с PIIFormatter и TextFormatter
- Structured logging (JSON для prod, text для dev)
- PII masking (emails, tokens, phone numbers)
- Log rotation (по размеру и времени)
- Context injection (user_id, request_id)
- Колоризация для консоли (dev mode)
- Интеграция с конфигурацией (Settings)
- Unit тесты для logging

### Out of Scope:
- Remote logging (ELK, Loki) — только placeholders
- Advanced filtering (будет позже)
- Custom handlers (будет позже)

## Plan (TDD: Red → Green → Refactor)

### Phase 1: Red (Tests)
1. Создать `tests/unit/test_logging.py`:
   - Тест для logger creation
   - Тест для JSON formatter
   - Тест для Text formatter
   - Тест для PII masking (emails, tokens)
   - Тест для log levels
2. Запустить тесты: `pytest tests/unit/test_logging.py -v` (все должны FAIL)

### Phase 2: Green (Implementation)
3. Создать `src/core/logging.py`:
   ```python
   import logging
   import json
   import re
   import sys
   from typing import Any, Dict
   from datetime import datetime
   from src.core.config import get_settings

   class PIIFormatter(logging.Formatter):
       """JSON formatter with PII masking for production"""

       def format(self, record: logging.LogRecord) -> str:
           log_dict = self._format_record(record)
           return json.dumps(log_dict, ensure_ascii=False)

       def _format_record(self, record: logging.LogRecord) -> Dict[str, Any]:
           return {
               "timestamp": datetime.utcnow().isoformat(),
               "level": record.levelname,
               "logger": record.name,
               "message": self._mask_pii(record.getMessage()),
               "module": record.module,
               "line": record.lineno,
               "function": record.funcName,
           }

       def _mask_pii(self, message: str) -> str:
           # Mask emails
           email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
           message = re.sub(email_pattern, '[EMAIL]', message)

           # Mask tokens/API keys (long alphanumeric strings)
           token_pattern = r'\b[A-Za-z0-9_-]{20,}\b'
           message = re.sub(token_pattern, '[TOKEN]', message)

           # Mask phone numbers (basic pattern)
           phone_pattern = r'\b\d{10,15}\b'
           message = re.sub(phone_pattern, '[PHONE]', message)

           return message


   class TextFormatter(logging.Formatter):
       """Text formatter with colors for development"""

       COLORS = {
           "DEBUG": "\033[36m",      # Cyan
           "INFO": "\033[32m",       # Green
           "WARNING": "\033[33m",    # Yellow
           "ERROR": "\033[31m",      # Red
           "CRITICAL": "\033[35m",   # Magenta
           "RESET": "\033[0m",
       }

       def format(self, record: logging.LogRecord) -> str:
           level = record.levelname
           color = self.COLORS.get(level, "")
           reset = self.COLORS["RESET"]

           formatted = f"{color}{level}{reset} | {record.name} | {record.getMessage()}"
           return formatted


   def setup_logging():
       """Setup logging based on configuration"""
       settings = get_settings()
       logger = logging.getLogger()
       logger.setLevel(getattr(logging, settings.log_level.upper()))

       # Remove existing handlers
       logger.handlers.clear()

       # Create handler
       handler = logging.StreamHandler(sys.stdout)
       handler.setLevel(getattr(logging, settings.log_level.upper()))

       # Choose formatter
       if settings.debug:
           formatter = TextFormatter()
       else:
           formatter = PIIFormatter()

       handler.setFormatter(formatter)
       logger.addHandler(handler)

       return logger
   ```
4. Обновить `src/core/__init__.py` для экспорта `setup_logging`
5. Запустить тесты: `pytest tests/unit/test_logging.py -v` (все должны PASS)

### Phase 3: Refactor
6. Добавить log rotation handler (дополнительно):
   ```python
   from logging.handlers import RotatingFileHandler

   def add_file_handler(logger, filename, max_bytes=10485760, backup_count=5):
       """Add rotating file handler"""
       handler = RotatingFileHandler(
           filename=filename,
           maxBytes=max_bytes,  # 10MB
           backupCount=backup_count,
       )
       handler.setFormatter(PIIFormatter())
       logger.addHandler(handler)
   ```
7. Refactor тесты: улучшить coverage, добавить edge cases для PII masking
8. Запустить `pytest tests/unit/test_logging.py -v --cov=src/core/logging --cov-report=term-missing` (должен быть ≥ 80%)

### Phase 4: Integration
9. Тестировать в dev mode:
   ```python
   import os
   os.environ["DEBUG"] = "True"
   from src.core.logging import setup_logging
   logger = setup_logging()
   logger.info("Test message in dev mode")
   ```
10. Тестировать в prod mode (JSON):
    ```python
    import os
    os.environ["DEBUG"] = "False"
    from src.core.logging import setup_logging
    logger = setup_logging()
    logger.info("Test message in prod mode")
    ```
11. Commit: `git add . && git commit -m "feat: implement logging with PII masking and structured output"`

## Files Allowlist
- `src/core/logging.py` (новый файл)
- `tests/unit/test_logging.py` (новый файл)
- `src/core/__init__.py` (обновление — экспорт setup_logging)
- `.env.example` (опционально — добавить LOG_LEVEL, LOG_FORMAT если нет)

## Definition of Done (DoD)
- [x] `src/core/logging.py` создан с PIIFormatter и TextFormatter
- [x] JSON formatter работает для production mode (DEBUG=False)
- [x] Text formatter с цветами работает для development mode (DEBUG=True)
- [x] PII masking работает:
  - Emails маскируются как `[EMAIL]`
  - Tokens маскируются как `[TOKEN]`
  - Phone numbers маскируются как `[PHONE]`
- [x] Log levels настраиваются через LOG_LEVEL (.env)
- [x] Log rotation handler (опционально)
- [x] Unit тесты созданы и проходят:
  - Logger creation (PASS)
  - JSON formatter (PASS)
  - Text formatter (PASS)
  - PII masking (PASS)
  - Log levels (PASS)
- [x] Coverage ≥ 80% для `src/core/logging.py`
- [x] Type hints для всех функций
- [x] Mypy не ругается на код
- [x] Commit сделан

## Risks / Edge Cases
- **JSON serialization:** некоторые объекты могут не быть JSON serializable
- **PII over-masking:** regex может замаскировать ложные positives (например, обычный текст похожий на токен)
- **Color codes на Windows:** могут не работать корректно без colorama
- **Log rotation:** файлы могут занять много места если не очищать

## How to Verify
```bash
# Unit тесты
pytest tests/unit/test_logging.py -v
pytest tests/unit/test_logging.py --cov=src/core/logging --cov-report=term-missing

# Type check
mypy src/core/logging.py

# Manual проверка (dev mode)
DEBUG=True python -c "from src.core.logging import setup_logging; logger = setup_logging(); logger.info('Test')"

# Manual проверка (prod mode)
DEBUG=False python -c "from src.core.logging import setup_logging; logger = setup_logging(); logger.info('test@example.com')"

# Проверка PII masking
python -c "from src.core.logging import PIIFormatter; f = PIIFormatter(); print(f.format(logging.LogRecord('test', 20, '', 0, 'Email: test@example.com', (), None)))"
```

## Dependencies
- Task 001: Git & GitHub Setup (должен быть завершён)
- Task 002: Virtual Environment Setup (должен быть завершён)
- Task 003: Project Structure Setup (должен быть завершён)
- Task 004: Configuration Management (должен быть завершён)

## Estimated Time
2-3 часа

## Notes
- Использовать `ensure_ascii=False` для JSON для поддержки русского языка
- PII masking — это только первый уровень защиты, секреты не должны попадать в логи
- Log rotation важна для предотвращения заполнения диска
- Цвета на Windows могут потребовать `import colorama; colorama.init()`
- Structured logging упрощает интеграцию с ELK/Loki в будущем
