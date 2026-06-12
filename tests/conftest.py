"""Shared test fixtures."""

import pytest
from starlette.testclient import TestClient

from src.main import app
from src.config.database import Base, engine
from src.config.settings import settings


@pytest.fixture()
def client():
    """Provide a test client with a fresh database for each test.

    Yields:
        A configured TestClient instance with API key authentication.
    """
    Base.metadata.create_all(bind=engine)
    with TestClient(app, headers={"X-API-Key": settings.API_KEY}) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
