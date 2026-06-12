"""Application settings loaded from environment variables."""

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings.

    Attributes:
        APP_NAME: The name of the application.
        DATABASE_URL: The database connection URL.
        LOG_LEVEL: The logging level.
        API_KEY: The API key required for authenticated endpoints.
    """

    APP_NAME: str = "Device Registry"
    DATABASE_URL: str = "sqlite:///./app.db"
    LOG_LEVEL: str = "INFO"
    API_KEY: str = ""

    @validator("API_KEY")
    def api_key_must_not_be_empty(cls, v: str) -> str:  # noqa: N805
        """Raise an error if API_KEY is empty or the placeholder value."""
        if not v or v == "changeme":
            raise ValueError(
                "API_KEY must be set to a non-empty, non-default value. "
                "Set the API_KEY environment variable before starting the application."
            )
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
