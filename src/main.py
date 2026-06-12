"""Main FastAPI application entry point."""

from fastapi import FastAPI
from pydantic import BaseModel

from src.config.settings import settings
from src.config.logging_config import setup_logging

setup_logging()

app = FastAPI(title=settings.APP_NAME)


class HealthResponse(BaseModel):
    """Response model for the health check endpoint.

    Attributes:
        status: A string indicating the health status of the application.
    """

    status: str


@app.get("/health", response_model=HealthResponse, status_code=200)
def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns a simple status response to indicate the service is running.

    Returns:
        HealthResponse: A response object with status set to 'ok'.
    """
    return HealthResponse(status="ok")
