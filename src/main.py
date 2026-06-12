"""FastAPI application entry point."""

import logging

from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

from src.config.logging_config import setup_logging
from src.config.settings import settings
from src.routes.device_type_route import router as device_types_router
from src.routes.location_route import router as locations_router
from src.routes.device_route import router as devices_router

setup_logging()

logger = logging.getLogger(__name__)

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def _verify_api_key(api_key: str = Security(_api_key_header)) -> str:
    """Validate the API key from the request header.

    Args:
        api_key: The value of the X-API-Key header.

    Returns:
        The validated API key string.

    Raises:
        HTTPException: 401 if the API key is missing or invalid.
    """
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key


app = FastAPI(title="Device Registry")

app.include_router(device_types_router, dependencies=[Security(_verify_api_key)])
app.include_router(locations_router, dependencies=[Security(_verify_api_key)])
app.include_router(devices_router, dependencies=[Security(_verify_api_key)])


@app.get("/health", status_code=200)
def health_check() -> dict:
    """Check the health of the application.

    Returns:
        A dictionary with a 'status' key set to 'ok'.
    """
    return {"status": "ok"}
