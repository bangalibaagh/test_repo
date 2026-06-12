"""Logging configuration for JSON-formatted log output."""

import logging
import json
import traceback
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Custom logging formatter that outputs JSON-formatted log lines.

    Each log record is serialized to a JSON string containing the keys
    ``timestamp``, ``level``, ``name``, and ``message``.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string with timestamp, level, name, and message.
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


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger to emit JSON-formatted log lines.

    Args:
        level: The logging level to set on the root logger. Defaults to
            ``'INFO'``.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
