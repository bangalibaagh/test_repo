"""Pytest configuration and shared fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from src.config.database import Base, get_db
import src.models.device_type  # noqa: F401
import src.models.location  # noqa: F401
import src.models.device  # noqa: F401
from src.main import app

_test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

_TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


@pytest.fixture(scope="function")
def client():
    """Provide a test client with an in-memory SQLite database.

    Sets up the database schema before each test and tears it down
    afterwards. Overrides the ``get_db`` dependency so all database
    operations use the in-memory engine.

    Yields:
        A ``TestClient`` instance configured against the FastAPI app.
    """
    # model imports will be added by resource components

    Base.metadata.create_all(bind=_test_engine)

    def override_get_db():
        """Yield a database session bound to the in-memory test engine.

        Yields:
            A SQLAlchemy session for the in-memory SQLite database.
        """
        db = _TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=_test_engine)
    app.dependency_overrides.clear()
