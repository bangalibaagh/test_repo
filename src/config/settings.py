"""Application settings module.

This module defines the application configuration using pydantic-settings,
allowing settings to be overridden via environment variables or a .env file.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings

_ALLOWED_DB_SCHEMES = {"sqlite"}


class Settings(BaseSettings):
    """Application settings with defaults.

    Attributes:
        APP_NAME: The name of the application.
        DATABASE_URL: The SQLAlchemy database connection URL.
        LOG_LEVEL: The logging level for the application.
    """

    APP_NAME: str = "Device Registry"
    DATABASE_URL: str = "sqlite:///./app.db"
    LOG_LEVEL: str = "INFO"

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure DATABASE_URL uses an allowed scheme.

        Args:
            v: The raw DATABASE_URL string.

        Returns:
            The validated DATABASE_URL string.

        Raises:
            ValueError: If the scheme is not in the allowed set.
        """
        scheme = v.split("://")[0].lower() if "://" in v else ""
        if scheme not in _ALLOWED_DB_SCHEMES:
            raise ValueError(
                f"DATABASE_URL scheme '{scheme}' is not allowed. "
                f"Allowed schemes: {sorted(_ALLOWED_DB_SCHEMES)}"
            )
        return v

    class Config:
        """Pydantic config for Settings."""

        env_file = ".env"


settings = Settings()
