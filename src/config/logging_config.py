"""JSON logging configuration for the application.

This module provides a custom JSON log formatter and a helper function
to configure the root logger with JSON output.
"""

import logging
import json
from datetime import datetime, timezone


class _JsonFormatter(logging.Formatter):
    """Custom log formatter that emits JSON records.

    Each log record is serialised as a JSON object containing
    ``timestamp``, ``level``, and ``message`` fields.
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string with timestamp, level, and message.
        """
        log_entry = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)


def configure_logging(log_level: str = "INFO") -> None:
    """Configure the root logger to use JSON formatting.

    Args:
        log_level: The desired logging level (e.g. 'INFO', 'DEBUG').
    """
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
