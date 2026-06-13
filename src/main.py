"""FastAPI application entry point.

This module creates and configures the FastAPI application instance,
sets up JSON logging, and registers the health-check endpoint.
"""

from fastapi import FastAPI

from src.config.settings import settings
from src.config.logging_config import configure_logging

configure_logging(settings.LOG_LEVEL)

app = FastAPI(title=settings.APP_NAME)


@app.get("/health", response_model=dict, status_code=200)
def health_check() -> dict:
    """Return the health status of the application.

    Returns:
        A dictionary with a single ``status`` key set to ``'ok'``.
    """
    return {"status": "ok"}
