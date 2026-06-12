"""Logging configuration for JSON-formatted log output."""

import logging
import json
import time


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
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)


def setup_logging() -> None:
    """Configure the root logger to emit JSON-formatted log lines.

    Sets up a StreamHandler with the JsonFormatter and applies it to
    the root logger. The log level is set to INFO by default.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
