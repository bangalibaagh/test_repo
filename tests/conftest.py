"""Pytest configuration and shared fixtures."""

import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from typing import Generator

from src.config.database import Base, get_db
from src.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def client() -> Generator:
    """Provide a TestClient with an in-memory SQLite database.

    Creates all tables before the test and drops them after. Overrides the
    get_db dependency on the FastAPI app to use the in-memory test database.

    Yields:
        TestClient: A Starlette test client configured with the FastAPI app.
    """
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator:
        """Override get_db to use the in-memory test database.

        Yields:
            Session: A SQLAlchemy test database session.
        """
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()
