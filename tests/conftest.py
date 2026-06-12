"""Pytest configuration and shared fixtures."""

import pytest
from starlette.testclient import TestClient
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
    """Provide a test HTTP client backed by an in-memory SQLite database.

    This fixture:
    - Imports all resource models so ``Base.metadata`` is fully populated.
    - Creates all tables before each test.
    - Overrides the ``get_db`` dependency with a session bound to the
      in-memory engine.
    - Tears down all tables and clears dependency overrides after each test.

    Yields:
        A ``TestClient`` instance configured against the FastAPI application.
    """
    # resource model imports go here
    from src.models.device_type import DeviceType  # noqa: F401

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        """Yield a test database session.

        Yields:
            A SQLAlchemy session bound to the in-memory test engine.
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
