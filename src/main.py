"""FastAPI application entry point."""

from fastapi import FastAPI

from src.config.settings import settings
from src.config.logging_config import configure_logging
from src.routes.device_type_route import router as device_type_router

configure_logging(settings.LOG_LEVEL)

app = FastAPI(title=settings.APP_NAME)

app.include_router(device_type_router)


@app.get("/health", response_model=dict, status_code=200)
def health_check() -> dict:
    """Health check endpoint.

    Returns:
        A dictionary with a status key indicating the service is healthy.
    """
    return {"status": "ok"}
