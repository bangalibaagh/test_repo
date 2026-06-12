"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException

from src.config.logging_config import setup_logging
from src.config.settings import settings
from src.routers import device_types, devices, health, locations

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate critical settings at startup."""
    if not settings.API_KEY or settings.API_KEY == "changeme":
        raise RuntimeError(
            "API_KEY must be set to a non-empty, non-default value. "
            "Set the API_KEY environment variable before starting the application."
        )
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


def _verify_api_key(x_api_key: str = Header(default="")) -> None:
    """Verify the X-API-Key header matches the configured API key.

    Args:
        x_api_key: The value of the X-API-Key request header.

    Raises:
        HTTPException: 401 if the key is missing or does not match.
    """
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


app.include_router(health.router)
app.include_router(device_types.router)
app.include_router(devices.router)
app.include_router(locations.router)
