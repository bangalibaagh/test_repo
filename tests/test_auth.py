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

# Use in-memory SQLite with StaticPool to avoid file persistence
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


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_post_device_type_wrong_key_returns_403():
    """A wrong API key should return 403."""
    os.environ["API_KEY"] = "correct-key"
    try:
        response = client.post(
            "/device-types/",
            json={"name": "Sensor"},
            headers={"X-API-Key": "wrong-key"},
        )
        assert response.status_code == 403
    finally:
        del os.environ["API_KEY"]


def test_post_device_type_missing_key_returns_401():
    """A missing API key header should return 401."""
    os.environ["API_KEY"] = "correct-key"
    try:
        response = client.post(
            "/device-types/",
            json={"name": "Sensor"},
        )
        assert response.status_code == 401
    finally:
        del os.environ["API_KEY"]


def test_post_device_type_correct_key_returns_201():
    """A correct API key should return 201."""
    os.environ["API_KEY"] = "correct-key"
    try:
        response = client.post(
            "/device-types/",
            json={"name": "Sensor"},
            headers={"X-API-Key": "correct-key"},
        )
        assert response.status_code == 201
    finally:
        del os.environ["API_KEY"]


def test_post_device_missing_key_returns_401():
    """A missing API key header on device creation should return 401."""
    os.environ["API_KEY"] = "correct-key"
    try:
        response = client.post(
            "/devices/",
            json={
                "name": "Dev1",
                "serial_number": "SN-001",
            },
        )
        assert response.status_code == 401
    finally:
        del os.environ["API_KEY"]


def test_delete_device_type_missing_key_returns_401():
    """A missing API key header on device-type deletion should return 401."""
    os.environ["API_KEY"] = "correct-key"
    try:
        response = client.delete(
            "/device-types/999",
        )
        assert response.status_code == 401
    finally:
        del os.environ["API_KEY"]


def test_put_device_type_missing_key_returns_401():
    """A missing API key header on device-type update should return 401."""
    os.environ["API_KEY"] = "correct-key"
    try:
        response = client.put(
            "/device-types/999",
            json={"name": "Updated"},
        )
        assert response.status_code == 401
    finally:
        del os.environ["API_KEY"]


def test_no_api_key_configured_raises_403():
    """When API_KEY env var is not set, mutating endpoints must return 403.

    Security: an unset or empty API_KEY must NOT silently bypass auth.
    This replaces the old 'allows_post' behaviour which was a security hole.
    """
    # Ensure API_KEY is absent from the environment
    os.environ.pop("API_KEY", None)
    response = client.post(
        "/device-types/",
        json={"name": "Sensor"},
        headers={"X-API-Key": "any-key"},
    )
    # Server must refuse when no key is configured - 403 is the correct response
    assert response.status_code == 403


def test_empty_api_key_env_raises_403():
    """When API_KEY env var is set to empty string, mutating endpoints must return 403.

    Security: an empty-string API_KEY must NOT bypass auth.
    """
    os.environ["API_KEY"] = ""
    try:
        response = client.post(
            "/device-types/",
            json={"name": "Sensor"},
            headers={"X-API-Key": ""},
        )
        assert response.status_code == 403
    finally:
        del os.environ["API_KEY"]
