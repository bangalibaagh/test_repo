"""Shared pytest fixtures for the test suite."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def client():
    """Provide a TestClient with an in-memory SQLite database.

    Yields:
        TestClient: A FastAPI test client configured to use an in-memory
            SQLite database for isolation.
    """
    # resource model imports will be added here

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        """Override get_db dependency to use the in-memory test database.

        Yields:
            Session: A SQLAlchemy session bound to the in-memory engine.
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
