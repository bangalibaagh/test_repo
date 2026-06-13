"""Tests for API key authentication on mutating endpoints."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.device import Device  # noqa: F401 - ensure models are registered
from src.models.device_type import DeviceType  # noqa: F401
from src.models.location import Location  # noqa: F401

# Import Base and get_db using the same symbols as conftest.py / other tests.
# The project exposes these through src.models (declarative base) and src.routes (get_db).
try:
    from src.database import Base, get_db  # type: ignore[import]
except ModuleNotFoundError:
    try:
        from src.db import Base, get_db  # type: ignore[import,no-redef]
    except ModuleNotFoundError:
        # Fall back to the pattern used by conftest.py in this repo.
        from src.models.device import Device as _BaseCarrier
        Base = _BaseCarrier.metadata  # type: ignore[assignment]
        # get_db must come from wherever the app wires it; import from conftest pattern
        import importlib, sys
        # Try common route module locations
        for _mod in ("src.routes.devices", "src.routes", "src.main"):
            try:
                _m = importlib.import_module(_mod)
                if hasattr(_m, "get_db"):
                    get_db = _m.get_db  # type: ignore[assignment]
                    break
            except Exception:
                pass
        else:
            raise ImportError("Cannot locate get_db in the project")
        # Re-acquire Base from the model's registry
        Base = _BaseCarrier.__bases__[0] if hasattr(_BaseCarrier, '__bases__') else _BaseCarrier  # type: ignore[assignment]

DATABASE_URL = "sqlite:///./test_auth.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
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


def test_post_device_type_correct_key_succeeds(client, monkeypatch):
    """POST /device-types/ with correct API_KEY header succeeds."""
    monkeypatch.setenv("API_KEY", "secret")
    response = client.post("/device-types/", json={"name": "Sensor"}, headers={"X-API-Key": "secret"})
    assert response.status_code == 201


def test_delete_device_missing_key_returns_401(client, monkeypatch):
    """DELETE /devices/{id} with API_KEY set but no header returns 401."""
    # Create a device type and device first without auth (API_KEY not set yet)
    monkeypatch.delenv("API_KEY", raising=False)
    dt_resp = client.post("/device-types/", json={"name": "Sensor"})
    assert dt_resp.status_code == 201
    dt_id = dt_resp.json()["id"]

    dev_resp = client.post(
        "/devices/",
        json={"name": "Dev1", "serial_number": "SN-001", "device_type_id": dt_id},
    )
    assert dev_resp.status_code == 201
    dev_id = dev_resp.json()["id"]

    # Now enable auth and try to delete without a key
    monkeypatch.setenv("API_KEY", "secret")
    response = client.delete(f"/devices/{dev_id}")
    assert response.status_code == 401


def test_delete_device_wrong_key_returns_403(client, monkeypatch):
    """DELETE /devices/{id} with API_KEY set but wrong header returns 403."""
    monkeypatch.delenv("API_KEY", raising=False)
    dt_resp = client.post("/device-types/", json={"name": "Sensor2"})
    assert dt_resp.status_code == 201
    dt_id = dt_resp.json()["id"]

    dev_resp = client.post(
        "/devices/",
        json={"name": "Dev2", "serial_number": "SN-002", "device_type_id": dt_id},
    )
    assert dev_resp.status_code == 201
    dev_id = dev_resp.json()["id"]

    monkeypatch.setenv("API_KEY", "secret")
    response = client.delete(f"/devices/{dev_id}", headers={"X-API-Key": "wrong"})
    assert response.status_code == 403
