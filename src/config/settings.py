"""Application settings module.

This module defines the application configuration using pydantic-settings,
allowing settings to be overridden via environment variables or a .env file.
"""

from pydantic_settings import BaseSettings


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

    class Config:
        """Pydantic config for Settings."""

        env_file = ".env"


settings = Settings()
