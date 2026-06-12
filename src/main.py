"""Main application module for the Device Registry FastAPI service.

This module initialises the FastAPI application, configures JSON-structured
logging on startup, and registers the core HTTP endpoints.
"""

import json
import logging
import sys
from datetime import datetime, timezone

from fastapi import FastAPI

from src.config.settings import settings


class _JsonFormatter(logging.Formatter):
    """Custom log formatter that emits records as JSON objects.

    Each log record is serialised to a single-line JSON string containing
    the keys ``timestamp``, ``level``, ``message``, and ``logger``.
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: D102
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string representing the log record.
        """
        payload = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(payload)


def _configure_logging() -> None:
    """Configure the root logger to emit JSON-structured log records.

    Attaches a ``StreamHandler`` writing to *stdout* with the
    ``_JsonFormatter`` formatter. The log level is taken from
    ``settings.LOG_LEVEL``.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))


app = FastAPI(title=settings.APP_NAME)
"""The FastAPI application instance for the Device Registry service."""


@app.on_event("startup")
async def _startup_event() -> None:  # noqa: D401
    """FastAPI startup handler that initialises JSON structured logging."""
    _configure_logging()
    logging.getLogger(__name__).info("Application startup complete.")


@app.get("/health", status_code=200)
async def health_check() -> dict:
    """Return a simple health-check response.

    Returns:
        A dictionary with a single key ``status`` set to ``'ok'``.
    """
    return {"status": "ok"}
