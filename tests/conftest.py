"""Shared test fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.main import app
from src.config.database import Base, get_db

# Use a fixed non-empty API key for tests so the startup validator passes.
TEST_API_KEY = "test-api-key-for-pytest"


@pytest.fixture(autouse=True)
def _patch_api_key(monkeypatch):
    """Override the API_KEY setting for every test."""
    import src.config.settings as _settings_mod
    monkeypatch.setattr(_settings_mod.settings, "API_KEY", TEST_API_KEY)
    import src.main as _main_mod
    monkeypatch.setattr(_main_mod.settings, "API_KEY", TEST_API_KEY)


@pytest.fixture()
def client(_patch_api_key):
    """Provide a test client with a fresh in-memory database for each test.

    Yields:
        A configured TestClient instance with API key authentication.
    """
    # Per-test in-memory SQLite engine for full isolation.
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, headers={"X-API-Key": TEST_API_KEY}) as c:
        yield c
    app.dependency_overrides.pop(get_db, None)
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
