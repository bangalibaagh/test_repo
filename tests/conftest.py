"""Pytest configuration and shared fixtures.

This module provides a reusable ``client`` fixture that spins up an
in-memory SQLite database for each test function and tears it down
afterwards.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from src.main import app
from src.config.database import Base, get_db

# Resource models must be imported here so Base.metadata registers their tables
# (imports added by each resource component)

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="function")
def client():
    """Provide a test HTTP client backed by an in-memory SQLite database.

    Yields:
        TestClient: A Starlette test client with the DB dependency overridden.
    """
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    def override_get_db():
        """Yield a test database session.

        Yields:
            Session: An active SQLAlchemy session bound to the test engine.
        """
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
