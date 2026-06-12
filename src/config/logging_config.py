"""Logging configuration for JSON-formatted log output."""

import logging
import json
import traceback
from datetime import datetime, timezone

from src.config.settings import settings


class JsonFormatter(logging.Formatter):
    """Custom logging formatter that emits JSON lines.

    Each log record is serialized as a single JSON object per line.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string representing the log record.
        """
        log_entry = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        if record.exc_info:
            log_entry["exception"] = traceback.format_exception(*record.exc_info)
        return json.dumps(log_entry)


def setup_logging() -> None:
    """Configure the root logger to emit JSON-formatted log lines.

    Uses the LOG_LEVEL from application settings to set the logging level.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    root_logger.handlers = []
    root_logger.addHandler(handler)
