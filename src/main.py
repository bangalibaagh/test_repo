"""Main application module.

Creates the FastAPI application instance, configures JSON-structured
logging, and registers core endpoints.
"""

import json
import logging
import sys
from datetime import datetime, timezone

from fastapi import FastAPI


class _JsonFormatter(logging.Formatter):
    """Custom JSON log formatter.

    Emits log records as JSON objects with level, message, and timestamp.
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-encoded string representing the log entry.
        """
        log_entry = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }
        return json.dumps(log_entry)


def _configure_logging() -> None:
    """Configure JSON-structured logging for the application.

    Sets up a stream handler on the root logger that emits JSON-formatted
    log records to stdout.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_JsonFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [handler]


_configure_logging()

app = FastAPI(title="App", version="0.1.0")

from src.routes.device_type_route import router as device_type_router  # noqa: E402
from src.routes.location_route import router as location_router  # noqa: E402

app.include_router(device_type_router)
app.include_router(location_router)


@app.get("/health", status_code=200)
def health_check() -> dict:
    """Health check endpoint.

    Returns:
        A dictionary with a status key indicating the service is running.
    """
    return {"status": "ok"}
