"""Main application module for the Device Registry API.

This module initialises the FastAPI application, configures JSON-formatted
logging, and registers core routes including the health-check endpoint.

Typical usage::

    uvicorn src.main:app --reload
"""

import logging
import json
from datetime import datetime, timezone

from fastapi import FastAPI

from src.routes.device_type_route import router as device_type_router
from src.routes.location_route import router as location_router
from src.routes.device_route import router as device_router


class _JsonFormatter(logging.Formatter):
    """Logging formatter that emits records as JSON strings.

    Each log record is serialised to a JSON object with the keys
    ``level``, ``message``, and ``timestamp``.
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: D102
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }
        return json.dumps(log_record)


def _configure_logging() -> None:
    """Configure application-wide JSON logging."""
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO)


_configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="Device Registry")

app.include_router(device_type_router)
app.include_router(location_router)
app.include_router(device_router)

logger.info("Device Registry application starting up")


@app.get("/health", response_model=dict, status_code=200)
def health_check() -> dict:
    """Return the health status of the application.

    Returns:
        dict: A dictionary with key ``status`` set to ``'ok'``.
    """
    return {"status": "ok"}
