"""Application settings module.

Defines the Settings class using pydantic-settings BaseSettings
and provides a module-level settings instance.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings.

    Attributes:
        DATABASE_URL: The database connection URL.
    """

    DATABASE_URL: str = "sqlite:///./app.db"

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate the DATABASE_URL field.

        Args:
            v: The database URL string to validate.

        Returns:
            The validated database URL string.

        Raises:
            ValueError: If the URL scheme is not supported.
        """
        allowed_schemes = ("sqlite", "postgresql", "postgresql+psycopg2", "mysql", "mysql+pymysql")
        scheme = v.split("://")[0] if "://" in v else ""
        if not any(scheme == s or scheme.startswith(s) for s in allowed_schemes):
            raise ValueError(
                f"DATABASE_URL scheme '{scheme}' is not supported. "
                f"Allowed schemes: {allowed_schemes}"
            )
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
