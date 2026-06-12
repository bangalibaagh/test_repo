"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings.

    Attributes:
        APP_NAME: The name of the application.
        DATABASE_URL: The database connection URL.
        LOG_LEVEL: The logging level.
        API_KEY: The API key required for authenticated endpoints.
            Must be set to a non-empty, non-default value via the
            API_KEY environment variable before starting the application.
    """

    APP_NAME: str = "Device Registry"
    DATABASE_URL: str = "sqlite:///./app.db"
    LOG_LEVEL: str = "INFO"
    # Default is empty string (not 'changeme') so the app refuses all
    # requests when unconfigured rather than accepting a known placeholder.
    API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
