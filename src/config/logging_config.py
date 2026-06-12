"""Logging configuration for JSON-formatted log output."""

import json
import logging

from src.config.settings import settings


class _JsonFormatter(logging.Formatter):
    """A logging formatter that emits JSON-formatted log lines.

    Attributes:
        None
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string representing the log record.
        """
        log_object = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_object["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_object)


def setup_logging() -> None:
    """Configure the root logger to emit JSON-formatted log lines.

    Sets up a StreamHandler with a JSON formatter. The log level is read
    from the application settings.

    Returns:
        None
    """
    logger = logging.getLogger()
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    formatter = _JsonFormatter()

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        for handler in logger.handlers:
            handler.setFormatter(formatter)
