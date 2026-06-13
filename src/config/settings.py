"""Application settings using pydantic-settings.

This module defines the Settings class and exports a module-level
instance for use throughout the application.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings.

    Attributes:
        APP_NAME: The name of the application.
        DATABASE_URL: The SQLAlchemy database connection URL.
        LOG_LEVEL: The logging level for the application.
    """

    APP_NAME: str = "Device Registry"
    DATABASE_URL: str = "sqlite:///./app.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        """Pydantic configuration."""

        env_file = ".env"


settings = Settings()
