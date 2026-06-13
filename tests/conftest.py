"""Shared test fixtures for the Device Registry test suite."""

# Resource model imports — add here as resources are built
# e.g. from src.models.device_type import DeviceType  # noqa: F401

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from src.config.database import Base, get_db
from src.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_session():
    """Yield a database session bound to the in-memory test engine.

    Yields:
        Session: A SQLAlchemy session for the in-memory SQLite database.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Return a TestClient with the get_db dependency overridden.

    Args:
        db_session: The in-memory database session fixture.

    Yields:
        TestClient: A Starlette test client configured to use the test database.
    """

    def override_get_db():
        """Override get_db to use the in-memory test session."""
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
