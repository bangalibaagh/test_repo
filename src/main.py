"""FastAPI application entry point."""

import logging

from fastapi import FastAPI

from src.config.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="Device Registry")


@app.get("/health", status_code=200)
def health_check() -> dict:
    """Check the health of the application.

    Returns:
        A dictionary with a 'status' key set to 'ok'.
    """
    return {"status": "ok"}
