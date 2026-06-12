"""Logging configuration for JSON-formatted log output."""

import logging
import json
import traceback
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Custom logging formatter that outputs log records as JSON strings.

    Each log line is a JSON object with keys: timestamp, level, name, message.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string representing the log record.
        """
        log_entry = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = traceback.format_exception(*record.exc_info)
        return json.dumps(log_entry)


def setup_logging() -> None:
    """Configure the root logger to emit JSON-formatted log lines.

    Sets up a StreamHandler with JsonFormatter on the root logger and
    applies the log level from application settings.
    """
    from src.config.settings import settings

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    if not root_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        root_logger.addHandler(handler)
    else:
        for handler in root_logger.handlers:
            handler.setFormatter(JsonFormatter())
