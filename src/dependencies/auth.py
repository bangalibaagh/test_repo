"""Authentication dependencies for FastAPI routes.

This module provides an API key dependency that can be applied to
mutating endpoints to enforce basic access control.
"""

import os

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

_API_KEY_NAME = "X-API-Key"
_api_key_header = APIKeyHeader(name=_API_KEY_NAME, auto_error=False)


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
    # Re-read from environment each call so tests can set API_KEY at runtime.
    # Use sentinel None to distinguish "not configured" from "set to empty string".
    effective_key = os.environ.get("API_KEY")  # None if unset, str if set

    # Security: both unset and empty-string API_KEY are treated as
    # misconfigured. Neither bypasses authentication. This prevents accidental
    # auth disable in production when the env var is missing or blank.
    if not effective_key:  # covers None and ""
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key not configured on server",
        )
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )
    if api_key != effective_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key
