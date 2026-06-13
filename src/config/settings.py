"""Application settings module.

This module defines the application configuration using pydantic_settings.
All fields have defaults so importing never raises.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with defaults.

    Attributes:
        DATABASE_URL: The database connection URL.
        APP_NAME: The name of the application.
    """

    DATABASE_URL: str = "sqlite:///./app.db"
    APP_NAME: str = "Device Registry"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        extra = "ignore"


settings = Settings()
