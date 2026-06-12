"""FastAPI application entry point."""

import logging

from fastapi import FastAPI

from src.config.logging_config import setup_logging
from src.routes.device_type_route import router as device_types_router
from src.routes.location_route import router as locations_router

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="Device Registry")

app.include_router(device_types_router)
app.include_router(locations_router)


@app.get("/health", status_code=200)
def health_check() -> dict:
    """Check the health of the application.

    Returns:
        A dictionary with a 'status' key set to 'ok'.
    """
    return {"status": "ok"}
