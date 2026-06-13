"""Authentication dependencies for FastAPI routes.

This module provides an API key dependency that can be applied to
mutating endpoints to enforce basic access control.
"""

import logging
import os

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

_API_KEY_NAME = "X-API-Key"
_api_key_header = APIKeyHeader(name=_API_KEY_NAME, auto_error=False)

logger = logging.getLogger(__name__)


def require_api_key(api_key: str = Security(_api_key_header)) -> str:
    """Validate the API key supplied in the X-API-Key request header.

    Behaviour:
    - If ``API_KEY`` env var is **not set** (``None``): authentication is
      disabled and all callers are permitted.  A warning is emitted so that
      operators notice the open configuration.
    - If ``API_KEY`` env var is set to an **empty string**: the server is
      considered *misconfigured* and every request is rejected with 403.
      This prevents an accidentally-blank env var from silently disabling
      auth when a real key was intended.
    - Otherwise the header value must match the configured key exactly.

    Args:
        api_key: The value extracted from the X-API-Key header.

    Returns:
        The validated API key string, or ``""`` when auth is disabled.

    Raises:
        HTTPException: 403 if ``API_KEY`` is set to an empty string
            (misconfigured server).
        HTTPException: 401 if no API key header is provided and a key is
            required.
        HTTPException: 403 if the supplied API key does not match.
    """
    # Re-read from environment each call so tests can set API_KEY at runtime.
    # Use os.environ.get to distinguish None (unset) from "" (set to empty).
    effective_key = os.environ.get("API_KEY")  # None if unset, str if set

    if effective_key is None:
        # No API_KEY configured: auth is intentionally disabled.
        # Emit a warning so operators are aware.
        logger.warning(
            "API_KEY environment variable is not set; "
            "authentication is disabled for all mutating endpoints."
        )
        return ""

    if effective_key == "":
        # API_KEY is explicitly set to an empty string — treat as
        # misconfiguration rather than silently disabling auth.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key not configured on server (empty API_KEY)",
        )

    # A real key is configured — enforce it.
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
