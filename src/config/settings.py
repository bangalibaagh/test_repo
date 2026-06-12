"""Application settings module."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings.

    Attributes:
        APP_NAME: The name of the application.
        DATABASE_URL: The database connection URL.
        LOG_LEVEL: The logging level for the application.
    """

    APP_NAME: str = "Device Registry"
    DATABASE_URL: str = "sqlite:///./app.db"
    LOG_LEVEL: str = "INFO"


settings = Settings()
