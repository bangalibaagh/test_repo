"""Logging configuration for JSON-formatted log output."""

import logging

from pythonjsonlogger import jsonlogger

from src.config.settings import settings


def setup_logging() -> None:
    """Configure the root logger to emit JSON-formatted log lines.

    Sets up a StreamHandler with a JSON formatter using python-json-logger.
    The log level is read from the application settings.

    Returns:
        None
    """
    logger = logging.getLogger()
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        for handler in logger.handlers:
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
            )
            handler.setFormatter(formatter)
