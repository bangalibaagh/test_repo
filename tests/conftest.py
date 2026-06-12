"""Shared pytest fixtures for the test suite."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.main import app


@pytest.fixture(scope="function")
def client():
    """Provide a TestClient backed by an in-memory SQLite database.

    Sets up a fresh in-memory SQLite database for each test function,
    overrides the FastAPI dependency for get_db, and tears down the
    database after the test completes.

    Yields:
        TestClient: A FastAPI test client configured with the in-memory database.
    """
    from src.models.device_type import DeviceType  # noqa: F401
    from src.models.location import Location  # noqa: F401

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        """Yield a test database session using the in-memory engine.

        Yields:
            Session: A SQLAlchemy database session bound to the in-memory engine.
        """
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
