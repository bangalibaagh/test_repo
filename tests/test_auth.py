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

# Import Base and get_db using the same pattern as conftest.py.
# conftest.py imports Base from src.models.base (or similar) and get_db from src.database.
import importlib

# Locate Base
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
    # Fall back: grab from the Device model's declarative base
    from src.models.device import Device as _D
    # Walk MRO to find the declarative base
    import sqlalchemy.orm as _sa_orm
    for _cls in type(_D).__mro__:
        if hasattr(_cls, 'metadata') and hasattr(_cls, 'registry'):
            _Base = _cls
            break
    if _Base is None:
        _Base = _D.__class__

Base = _Base  # type: ignore[assignment]

# Locate get_db
_get_db = None
for _gdb_mod in ("src.database", "src.db", "src.dependencies.database", "src.routes.devices", "src.routes", "src.main"):
    try:
        _m2 = importlib.import_module(_gdb_mod)
        if hasattr(_m2, "get_db"):
            _get_db = _m2.get_db
            break
    except Exception:
        pass

if _get_db is None:
    raise ImportError("Cannot locate get_db in the project")

get_db = _get_db  # type: ignore[assignment]

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
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_post_device_type_missing_key_returns_401(client, monkeypatch):
    """POST /device-types/ with API_KEY set but no header returns 401."""
    monkeypatch.setenv("API_KEY", "secret")
    response = client.post("/device-types/", json={"name": "Sensor"})
    assert response.status_code == 401


def test_post_device_type_wrong_key_returns_403(client, monkeypatch):
    """POST /device-types/ with API_KEY set but wrong header returns 403."""
    monkeypatch.setenv("API_KEY", "secret")
    response = client.post("/device-types/", json={"name": "Sensor"}, headers={"X-API-Key": "wrong"})
    assert response.status_code == 403


def test_post_device_type_correct_key_returns_201(client, monkeypatch):
    """POST /device-types/ with correct API_KEY returns 201."""
    monkeypatch.setenv("API_KEY", "secret")
    response = client.post("/device-types/", json={"name": "Sensor"}, headers={"X-API-Key": "secret"})
    assert response.status_code == 201


def test_post_device_missing_key_returns_401(client, monkeypatch):
    """POST /devices/ with API_KEY set but no header returns 401."""
    monkeypatch.setenv("API_KEY", "secret")
    response = client.post("/devices/", json={"name": "Dev", "serial_number": "SN1"})
    assert response.status_code == 401


def test_delete_device_type_missing_key_returns_401(client, monkeypatch):
    """DELETE /device-types/{id} with API_KEY set but no header returns 401."""
    monkeypatch.setenv("API_KEY", "secret")
    response = client.delete("/device-types/999")
    assert response.status_code == 401


def test_put_device_type_missing_key_returns_401(client, monkeypatch):
    """PUT /device-types/{id} with API_KEY set but no header returns 401."""
    monkeypatch.setenv("API_KEY", "secret")
    response = client.put("/device-types/999", json={"name": "Updated"})
    assert response.status_code == 401


def test_no_api_key_configured_allows_post(client, monkeypatch):
    """When API_KEY env var is not set, auth is disabled and POST succeeds."""
    monkeypatch.delenv("API_KEY", raising=False)
    response = client.post("/device-types/", json={"name": "Sensor"})
    # Auth disabled, so should not get 401/403
    assert response.status_code not in (401, 403)
