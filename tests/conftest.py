"""Pytest configuration and shared fixtures.

This module provides a reusable ``client`` fixture that spins up an in-memory
SQLite database using StaticPool, overrides the FastAPI ``get_db`` dependency,
and tears everything down after each test function.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from src.main import app
from src.config.database import Base, get_db

# resource model imports added per component
from src.models.device_type import DeviceType  # noqa: F401
from src.models.location import Location  # noqa: F401
from src.models.device import Device  # noqa: F401

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Yield a testing database session and ensure it is closed after use.

    Yields:
        Session: A SQLAlchemy database session bound to the in-memory engine.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Provide a configured TestClient with an isolated in-memory database.

    Creates all tables before the test, overrides the ``get_db`` dependency
    with an in-memory SQLite session, and cleans up after the test.

    Yields:
        TestClient: A Starlette test client pointed at the FastAPI app.
    """
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
