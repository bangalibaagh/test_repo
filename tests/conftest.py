"""Shared test fixtures and configuration.

Provides an in-memory SQLite engine and a function-scoped TestClient
fixture with dependency overrides for isolated database testing.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.config.database import Base, get_db
from src.main import app

# ---------------------------------------------------------------------------
# In-memory test database engine
# ---------------------------------------------------------------------------

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Provide a TestClient with an isolated in-memory database.

    Sets up all tables before each test and tears them down afterwards.
    Overrides the ``get_db`` dependency so every request uses the
    in-memory session instead of the production database.

    Yields:
        TestClient: A configured Starlette test client for the FastAPI app.
    """
    # Import resource models here so their tables are registered on
    # Base.metadata before create_all is called.  Expand this list as
    # new models are added to the project.
    from src.models.device import Device  # noqa: F401
    from src.models.device_type import DeviceType  # noqa: F401
    from src.models.location import Location  # noqa: F401

    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        """Override get_db to use the in-memory test session.

        Yields:
            Session: An active test database session.
        """
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
