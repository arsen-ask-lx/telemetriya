"""Structured logging with PII masking and context injection."""

import json
import logging
import re
import sys
from datetime import UTC, datetime
from typing import Any, Dict

from src.core.config import get_settings


class PIIFormatter(logging.Formatter):
    """JSON formatter with PII masking for production.

    Masks sensitive information:
    - Emails → [EMAIL]
    - Long tokens/API keys → [TOKEN]
    - Phone numbers → [PHONE]
    """

    # Patterns for PII detection
    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    TOKEN_PATTERN = re.compile(r"\b[A-Za-z0-9_-]{20,}\b")
    PHONE_PATTERN = re.compile(r"\b\d{10,15}\b")

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON with PII masking.

        Args:
            record: Log record to format

        Returns:
            JSON string with masked PII
        """
        log_dict = self._format_record(record)
        return json.dumps(log_dict, ensure_ascii=False)

    def _format_record(self, record: logging.LogRecord) -> Dict[str, Any]:
        """Convert log record to dictionary with masked message.

        Args:
            record: Log record to convert

        Returns:
            Dictionary with log fields
        """
        # Mask the message
        masked_message = self._mask_pii(record.getMessage())

        # Extract extra context if present
        extra = {
            key: value
            for key, value in record.__dict__.items()
            if key
            not in {
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "msg",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
            }
        }

        # Build log dict
        log_dict = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": masked_message,
            "module": record.module,
            "line": record.lineno,
            "function": record.funcName,
        }

        # Add extra context if available
        if extra:
            log_dict.update(extra)

        # Add exception info if present
        if record.exc_info:
            log_dict["exception"] = self.formatException(record.exc_info)

        return log_dict

    def _mask_pii(self, message: str) -> str:
        """Mask PII in message.

        Args:
            message: Message to mask

        Returns:
            Message with masked PII
        """
        if not message:
            return ""

        # Mask emails
        message = self.EMAIL_PATTERN.sub("[EMAIL]", message)

        # Mask tokens/API keys (long alphanumeric strings)
        message = self.TOKEN_PATTERN.sub("[TOKEN]", message)

        # Mask phone numbers (basic pattern)
        message = self.PHONE_PATTERN.sub("[PHONE]", message)

        return message


class TextFormatter(logging.Formatter):
    """Text formatter with colors for development.

    Uses ANSI color codes for console output.
    Colors work on Linux/Mac and modern Windows terminals.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colored level.

        Args:
            record: Log record to format

        Returns:
            Formatted string with ANSI colors
        """
        level = record.levelname
        color = self.COLORS.get(level, "")
        reset = self.COLORS["RESET"]

        # Format: LEVEL | logger | module:function:line | message
        formatted = (
            f"{color}{level}{reset} | "
            f"{record.name} | "
            f"{record.module}:{record.funcName}:{record.lineno} | "
            f"{record.getMessage()}"
        )

        return formatted


def setup_logging() -> logging.Logger:
    """Setup logging based on configuration.

    Returns:
        Configured root logger
    """
    settings = get_settings()

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create stream handler for stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    # Choose formatter based on debug mode
    formatter: logging.Formatter
    if settings.debug:
        formatter = TextFormatter()
    else:
        formatter = PIIFormatter()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a named logger.

    Convenience function for getting a logger with a specific name.

    Args:
        name: Name of the logger (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
