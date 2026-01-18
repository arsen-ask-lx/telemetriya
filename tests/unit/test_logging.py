"""Unit tests for logging module."""

import logging
import os
import sys
from io import StringIO

import pytest

# Mock config before importing logging module
os.environ["TELEGRAM_TOKEN"] = "test_token_12345678901234567890"
os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost/test"
os.environ["SECRET_KEY"] = "test_secret_key_12345678901234567890"

# Import formatter classes for type checking in tests
from src.core.logging import PIIFormatter, TextFormatter


def test_logger_creation():
    """Test that logger can be created."""
    from src.core.logging import setup_logging

    logger = setup_logging()

    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.level >= logging.INFO


def test_logger_has_handlers():
    """Test that logger has at least one handler."""
    from src.core.logging import setup_logging

    logger = setup_logging()

    assert len(logger.handlers) > 0


def test_log_level_debug():
    """Test that log level can be set to DEBUG."""
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["DEBUG"] = "True"

    # Force reload settings
    if "src.core.config" in sys.modules:
        del sys.modules["src.core.config"]
    if "src.core.logging" in sys.modules:
        del sys.modules["src.core.logging"]

    from src.core.logging import setup_logging

    logger = setup_logging()

    assert logger.level == logging.DEBUG

    # Cleanup
    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["DEBUG"] = "False"
    if "src.core.config" in sys.modules:
        del sys.modules["src.core.config"]
    if "src.core.logging" in sys.modules:
        del sys.modules["src.core.logging"]


def test_json_formatter_creation():
    """Test that PIIFormatter (JSON) can be created."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    assert formatter is not None


def test_json_formatter_output():
    """Test that PIIFormatter produces valid JSON."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)

    assert output is not None
    assert isinstance(output, str)

    # Try to parse as JSON
    import json

    parsed = json.loads(output)
    assert "message" in parsed
    assert "level" in parsed
    assert "timestamp" in parsed


def test_text_formatter_creation():
    """Test that TextFormatter can be created."""
    from src.core.logging import TextFormatter

    formatter = TextFormatter()
    assert formatter is not None


def test_text_formatter_output():
    """Test that TextFormatter produces colored text."""
    from src.core.logging import TextFormatter

    formatter = TextFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)

    assert output is not None
    assert isinstance(output, str)
    assert "INFO" in output
    assert "test" in output
    assert "Test message" in output


def test_pii_masking_email():
    """Test that emails are masked."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Contact: test@example.com",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    import json

    parsed = json.loads(output)

    assert "test@example.com" not in parsed["message"]
    assert "[EMAIL]" in parsed["message"]


def test_pii_masking_token():
    """Test that long alphanumeric tokens are masked."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    token = "abc123def456ghi789jkl012mno345pqr678"
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg=f"Token: {token}",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    import json

    parsed = json.loads(output)

    assert token not in parsed["message"]
    assert "[TOKEN]" in parsed["message"]


def test_pii_masking_phone():
    """Test that phone numbers are masked."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Phone: +79001234567",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    import json

    parsed = json.loads(output)

    assert "+79001234567" not in parsed["message"]
    assert "[PHONE]" in parsed["message"]


def test_pii_masking_multiple():
    """Test that multiple PII types are masked in one message."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Contact ivan@example.com, token: abc123def456ghi789jkl012mno345pqr678, phone: +79001234567",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    import json

    parsed = json.loads(output)

    assert "ivan@example.com" not in parsed["message"]
    assert "abc123def456ghi789jkl012mno345pqr678" not in parsed["message"]
    assert "+79001234567" not in parsed["message"]
    assert "[EMAIL]" in parsed["message"]
    assert "[TOKEN]" in parsed["message"]
    assert "[PHONE]" in parsed["message"]


def test_pii_no_false_positive_short_token():
    """Test that short alphanumeric strings are NOT masked."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="ID: abc123",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    import json

    parsed = json.loads(output)

    assert "abc123" in parsed["message"]  # Should NOT be masked
    assert "[TOKEN]" not in parsed["message"]


def test_dev_mode_uses_text_formatter():
    """Test that debug mode uses TextFormatter."""
    os.environ["DEBUG"] = "True"

    if "src.core.config" in sys.modules:
        del sys.modules["src.core.config"]
    if "src.core.logging" in sys.modules:
        del sys.modules["src.core.logging"]

    from src.core.logging import setup_logging, PIIFormatter

    logger = setup_logging()

    assert len(logger.handlers) > 0
    handler = logger.handlers[0]
    # Check by class name to avoid isinstance issues after module reload
    assert handler.formatter.__class__.__name__ == "TextFormatter"
    # Also verify it's NOT PIIFormatter
    assert not isinstance(handler.formatter, PIIFormatter)

    # Cleanup
    os.environ["DEBUG"] = "False"
    if "src.core.config" in sys.modules:
        del sys.modules["src.core.config"]
    if "src.core.logging" in sys.modules:
        del sys.modules["src.core.logging"]


def test_prod_mode_uses_pii_formatter():
    """Test that production mode uses PIIFormatter."""
    os.environ["DEBUG"] = "False"

    if "src.core.config" in sys.modules:
        del sys.modules["src.core.config"]
    if "src.core.logging" in sys.modules:
        del sys.modules["src.core.logging"]

    from src.core.logging import setup_logging

    logger = setup_logging()

    assert len(logger.handlers) > 0
    handler = logger.handlers[0]
    from src.core.logging import PIIFormatter

    assert isinstance(handler.formatter, PIIFormatter)

    # Cleanup
    if "src.core.config" in sys.modules:
        del sys.modules["src.core.config"]
    if "src.core.logging" in sys.modules:
        del sys.modules["src.core.logging"]


def test_context_injection():
    """Test that extra context is captured."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    # Add extra context
    record.user_id = "12345"
    record.request_id = "abc-def-ghi"

    output = formatter.format(record)
    import json

    parsed = json.loads(output)

    # Basic fields should be present
    assert "message" in parsed
    assert "level" in parsed
    assert parsed["message"] == "Test message"


def test_unicode_support():
    """Test that Unicode (Russian) is supported."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Тестовое сообщение на русском",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)

    assert output is not None
    assert "Тестовое сообщение на русском" in output
    # Should be valid JSON (not escape Unicode)
    import json

    parsed = json.loads(output)
    assert parsed["message"] == "Тестовое сообщение на русском"


def test_error_handling_invalid_json():
    """Test that logging handles edge cases gracefully."""
    from src.core.logging import PIIFormatter

    formatter = PIIFormatter()

    # Record with None message
    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname="test.py",
        lineno=1,
        msg=None,
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)

    # Should not crash
    assert output is not None
    import json

    parsed = json.loads(output)
    assert "message" in parsed
