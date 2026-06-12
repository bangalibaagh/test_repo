"""Tests for database engine configuration."""

import importlib
from unittest.mock import patch, MagicMock


def test_sqlite_url_sets_check_same_thread():
    """connect_args must include check_same_thread=False for SQLite URLs."""
    mock_settings = MagicMock()
    mock_settings.DATABASE_URL = "sqlite:///./test.db"

    created_engines = []

    def fake_create_engine(url, **kwargs):
        created_engines.append((url, kwargs))
        return MagicMock()

    with patch("src.config.settings.settings", mock_settings), \
         patch("src.config.database.settings", mock_settings), \
         patch("src.config.database.create_engine", fake_create_engine):
        import src.config.database as db_module
        importlib.reload(db_module)

    assert len(created_engines) == 1
    url, kwargs = created_engines[0]
    assert url == "sqlite:///./test.db"
    assert kwargs.get("connect_args", {}).get("check_same_thread") is False


def test_non_sqlite_url_does_not_set_check_same_thread():
    """connect_args must NOT include check_same_thread for non-SQLite URLs."""
    mock_settings = MagicMock()
    mock_settings.DATABASE_URL = "postgresql://user:pass@localhost/testdb"

    created_engines = []

    def fake_create_engine(url, **kwargs):
        created_engines.append((url, kwargs))
        return MagicMock()

    with patch("src.config.settings.settings", mock_settings), \
         patch("src.config.database.settings", mock_settings), \
         patch("src.config.database.create_engine", fake_create_engine):
        import src.config.database as db_module
        importlib.reload(db_module)

    assert len(created_engines) == 1
    url, kwargs = created_engines[0]
    assert url == "postgresql://user:pass@localhost/testdb"
    assert "check_same_thread" not in kwargs.get("connect_args", {})
