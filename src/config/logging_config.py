"""JSON structured logging configuration."""

import json
import logging


class _JsonFormatter(logging.Formatter):
    """Custom logging formatter that outputs log records as JSON.

    Formats each log record as a JSON object containing the timestamp,
    log level, logger name, and message.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-formatted string representation of the log record.
        """
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def configure_logging(log_level: str = "INFO") -> None:
    """Configure JSON structured logging for the application.

    Args:
        log_level: The logging level to set (e.g. 'INFO', 'DEBUG').
    """
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
