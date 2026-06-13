"""FastAPI application entry point.

This module initialises the FastAPI application, configures JSON logging,
registers the health endpoint, and provides a placeholder for routers.
"""

import logging
import json
from datetime import datetime, timezone

from fastapi import FastAPI

from src.config.settings import settings


class _JsonFormatter(logging.Formatter):
    """Custom JSON log formatter.

    Formats log records as single-line JSON objects suitable for structured
    log aggregation pipelines.
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: D102
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string representing the log record.
        """
        log_object = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_object["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_object)


def _configure_logging() -> None:
    """Configure application-wide JSON logging.

    Sets the root logger level and attaches a JSON-formatted stream handler
    based on the LOG_LEVEL setting.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.handlers = [handler]


_configure_logging()

app = FastAPI(title=settings.APP_NAME)

logger = logging.getLogger(__name__)


@app.get("/health", status_code=200, response_model=dict)
def health_check() -> dict:
    """Return the health status of the application.

    Returns:
        A dictionary with a single key ``status`` set to ``'ok'``.
    """
    logger.info("Health check requested")
    return {"status": "ok"}


# routers registered here
from src.routes.device_type_route import router as device_type_router  # noqa: E402

app.include_router(device_type_router)

from src.routes.location_route import router as location_router  # noqa: E402

app.include_router(location_router)
