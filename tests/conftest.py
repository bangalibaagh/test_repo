"""Pytest configuration and shared fixtures for the Device Registry test suite.

This module provides the ``client`` fixture, which spins up a temporary
in-memory SQLite database, creates all ORM tables, overrides the FastAPI
``get_db`` dependency, and tears everything down after each test function.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.main import app


@pytest.fixture(scope="function")
def client():
    """Provide a ``TestClient`` backed by a temporary in-memory SQLite database.

    The fixture performs the following steps:

    1. Creates a new SQLAlchemy engine pointing at an in-memory SQLite DB.
    2. Calls ``Base.metadata.create_all`` so all registered ORM models are
       present in the test database.
    3. Overrides the ``get_db`` FastAPI dependency with a generator that
       uses the test session factory.
    4. Yields a ``TestClient`` wrapping the application.
    5. Drops all tables and clears ``app.dependency_overrides`` on teardown.

    Yields:
        TestClient: A Starlette test client configured against the FastAPI app.
    """
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        """Yield a test database session and ensure it is closed afterward."""
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()
