"""Shared test fixtures."""

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

# Set API_KEY env var before importing app so settings loads a valid key.
TEST_API_KEY = "test-api-key-for-pytest"
os.environ.setdefault("API_KEY", TEST_API_KEY)

from src.main import app  # noqa: E402
from src.config.database import Base, get_db  # noqa: E402
from src.config.settings import settings  # noqa: E402

# Ensure the in-process settings object carries the test key.
settings.API_KEY = TEST_API_KEY


@pytest.fixture()
def client():
    """Provide a test client with a fresh in-memory database for each test.

    Yields:
        A configured TestClient instance with API key authentication.
    """
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
