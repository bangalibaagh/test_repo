"""Authentication dependencies for FastAPI routes.

This module provides an API key dependency that can be applied to
mutating endpoints to enforce basic access control.
"""

import os

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

_API_KEY_NAME = "X-API-Key"
_api_key_header = APIKeyHeader(name=_API_KEY_NAME, auto_error=False)

_API_KEY = os.environ.get("API_KEY", "")


def require_api_key(api_key: str = Security(_api_key_header)) -> str:
    """Validate the API key supplied in the X-API-Key request header.

    Args:
        api_key: The value extracted from the X-API-Key header.

    Returns:
        The validated API key string.

    Raises:
        HTTPException: 401 if no API key is provided.
        HTTPException: 403 if the API key is invalid.
    """
    if not _API_KEY:
        # If no API_KEY is configured, auth is disabled (dev/test mode).
        return ""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )
    if api_key != _API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key
