"""Pytest configuration and shared fixtures."""

import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.main import app

# resource model imports will be added by later components

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def client():
    """Provide a test client with an in-memory SQLite database.

    Sets up the database schema before each test and tears it down
    afterwards. Overrides the ``get_db`` dependency so all requests
    use the in-memory session.

    Yields:
        TestClient: A Starlette test client bound to the FastAPI app.
    """
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        """Yield a testing database session.

        Yields:
            Session: A SQLAlchemy session connected to the in-memory database.
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
