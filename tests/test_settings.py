"""Tests for application settings validation."""

import pytest
from pydantic import ValidationError

from src.config.settings import Settings


def test_validate_database_url_default_is_valid():
    """The default DATABASE_URL (sqlite) should pass validation."""
    s = Settings()
    assert s.DATABASE_URL.startswith("sqlite")


def test_validate_database_url_postgresql_is_valid():
    """A postgresql DATABASE_URL should pass validation."""
    s = Settings(DATABASE_URL="postgresql://user:pass@localhost/db")
    assert s.DATABASE_URL.startswith("postgresql")


def test_validate_database_url_invalid_scheme_raises():
    """An ftp:// DATABASE_URL should raise ValidationError."""
    with pytest.raises(ValidationError):
        Settings(DATABASE_URL="ftp://some-host/db")


def test_validate_database_url_redis_scheme_raises():
    """A redis:// DATABASE_URL should raise ValidationError."""
    with pytest.raises(ValidationError):
        Settings(DATABASE_URL="redis://localhost:6379/0")


def test_validate_log_level_default_is_valid():
    """The default LOG_LEVEL (INFO) should pass validation."""
    s = Settings()
    assert s.LOG_LEVEL == "INFO"


def test_validate_log_level_debug_is_valid():
    """DEBUG is a valid LOG_LEVEL."""
    s = Settings(LOG_LEVEL="DEBUG")
    assert s.LOG_LEVEL == "DEBUG"


def test_validate_log_level_case_insensitive():
    """LOG_LEVEL validation should normalise to uppercase."""
    s = Settings(LOG_LEVEL="warning")
    assert s.LOG_LEVEL == "WARNING"


def test_validate_log_level_invalid_raises():
    """An unrecognised LOG_LEVEL should raise ValidationError."""
    with pytest.raises(ValidationError):
        Settings(LOG_LEVEL="VERBOSE")


def test_validate_log_level_numeric_string_raises():
    """A numeric string LOG_LEVEL should raise ValidationError."""
    with pytest.raises(ValidationError):
        Settings(LOG_LEVEL="10")
