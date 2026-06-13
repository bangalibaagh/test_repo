"""Tests for API key authentication on mutating endpoints."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models.device import Device  # noqa: F401 - ensure models are registered
from src.models.device_type import DeviceType  # noqa: F401
from src.models.location import Location  # noqa: F401

# Import Base using the same pattern as conftest.py.
import importlib

# Locate Base - try known module paths first
_Base = None
for _base_mod in ("src.models.base", "src.database", "src.db"):
    try:
        _m = importlib.import_module(_base_mod)
        if hasattr(_m, "Base"):
            _Base = _m.Base
            break
    except Exception:
        pass

if _Base is None:
    # Fall back: grab from the Device model's declarative base via __bases__
    from src.models.device import Device as _D
    # The declarative base is the class that has both 'metadata' and 'registry'
    # It's accessible via Device's MRO - look for a class with metadata attr
    for _cls in type(_D).__mro__:
        if hasattr(_cls, 'metadata') and hasattr(_cls, 'registry'):
            _Base = _cls
            break
    if _Base is None:
        # Try getting it from the instance's class hierarchy
        for _cls in _D.__mro__:
            if hasattr(_cls, 'metadata') and hasattr(_cls, 'registry'):
                _Base = _cls
                break

if _Base is None:
    raise ImportError("Cannot locate declarative Base in the project")

Base = _Base  # type: ignore[assignment]

# Locate get_db - search all likely modules
_get_db = None
for _gdb_mod in (
    "src.database",
    "src.db",
    "src.dependencies.database",
    "src.dependencies.db",
    "src.routes.devices",
    "src.routes.device_types",
    "src.routes",
    "src.main",
):
    try:
        _m2 = importlib.import_module(_gdb_mod)
        if hasattr(_m2, "get_db"):
            _get_db = _m2.get_db
            break
    except Exception:
        pass

if _get_db is None:
    import pkgutil
    import src
    for _importer, _modname, _ispkg in pkgutil.walk_packages(
        path=src.__path__, prefix="src.", onerror=lambda x: None
    ):
        try:
            _m3 = importlib.import_module(_modname)
            if hasattr(_m3, "get_db"):
                _get_db = _m3.get_db
                break
        except Exception:
            pass

if _get_db is None:
    raise ImportError("Cannot locate get_db in the project")

get_db = _get_db  # type: ignore[assignment]

# Use in-memory SQLite with StaticPool to avoid file persistence and
# ensure all connections within the same process share the same database.
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def auth_client():
    """TestClient with API_KEY set to a known value."""
    os.environ["API_KEY"] = "test-secret"
    with TestClient(app) as c:
        yield c
    # Clean up: remove the key so subsequent tests start without it
    os.environ.pop("API_KEY", None)


@pytest.fixture()
def no_auth_client():
    """TestClient with API_KEY unset (auth disabled)."""
    os.environ.pop("API_KEY", None)
    with TestClient(app) as c:
        yield c


def test_post_device_type_wrong_key_returns_403(auth_client):
    """POST /device-types/ with wrong key returns 403.

    Args:
        auth_client: TestClient fixture with API_KEY configured.
    """
    response = auth_client.post(
        "/device-types/",
        json={"name": "Sensor", "description": "A sensor"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 403


def test_post_device_type_missing_key_returns_401(auth_client):
    """POST /device-types/ with no key header returns 401.

    Args:
        auth_client: TestClient fixture with API_KEY configured.
    """
    response = auth_client.post(
        "/device-types/",
        json={"name": "Sensor", "description": "A sensor"},
    )
    assert response.status_code == 401


def test_post_device_type_correct_key_returns_201(auth_client):
    """POST /device-types/ with correct key returns 201.

    Args:
        auth_client: TestClient fixture with API_KEY configured.
    """
    response = auth_client.post(
        "/device-types/",
        json={"name": "Sensor", "description": "A sensor"},
        headers={"X-API-Key": "test-secret"},
    )
    assert response.status_code == 201


def test_post_device_missing_key_returns_401(auth_client):
    """POST /devices/ with no key header returns 401.

    Args:
        auth_client: TestClient fixture with API_KEY configured.
    """
    response = auth_client.post(
        "/devices/",
        json={"name": "Dev1", "serial_number": "SN-001"},
    )
    assert response.status_code == 401


def test_delete_device_type_missing_key_returns_401(auth_client):
    """DELETE /device-types/{id} with no key header returns 401.

    Args:
        auth_client: TestClient fixture with API_KEY configured.
    """
    response = auth_client.delete("/device-types/999")
    assert response.status_code == 401


def test_put_device_type_missing_key_returns_401(auth_client):
    """PUT /device-types/{id} with no key header returns 401.

    Args:
        auth_client: TestClient fixture with API_KEY configured.
    """
    response = auth_client.put(
        "/device-types/999",
        json={"name": "Updated"},
    )
    assert response.status_code == 401


def test_no_api_key_configured_allows_post(no_auth_client):
    """POST /device-types/ succeeds when API_KEY env var is not set.

    When no API_KEY is configured the server operates in open mode and
    all mutating requests are permitted without credentials.

    Args:
        no_auth_client: TestClient fixture with API_KEY unset.
    """
    response = no_auth_client.post(
        "/device-types/",
        json={"name": "OpenSensor", "description": "No auth needed"},
    )
    assert response.status_code == 201


def test_empty_string_api_key_returns_403(no_auth_client):
    """POST /device-types/ returns 403 when API_KEY is set to empty string.

    An explicitly empty API_KEY is treated as a misconfiguration rather
    than 'no auth configured', so every request is rejected.

    Args:
        no_auth_client: TestClient fixture (API_KEY starts unset).
    """
    os.environ["API_KEY"] = ""
    try:
        response = no_auth_client.post(
            "/device-types/",
            json={"name": "Sensor", "description": "Should be blocked"},
        )
        assert response.status_code == 403
    finally:
        os.environ.pop("API_KEY", None)
