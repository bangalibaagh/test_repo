"""FastAPI application entry point."""

import logging

from fastapi import FastAPI
from pydantic import BaseModel

from src.config.logging_config import setup_logging
from src.config.settings import settings

setup_logging(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)


class HealthResponse(BaseModel):
    """Response model for the health check endpoint.

    Attributes:
        status: A string indicating the health status of the application.
    """

    status: str


@app.get("/health", response_model=HealthResponse, status_code=200)
def health_check() -> HealthResponse:
    """Return the health status of the application.

    Returns:
        A HealthResponse with status set to 'ok'.
    """
    logger.info("Health check requested")
    return HealthResponse(status="ok")
