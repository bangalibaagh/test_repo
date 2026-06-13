"""Tests for API key authentication on mutating endpoints."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app

# Import Base and get_db from wherever the app defines them.
# Try src.db first (common pattern), fall back to src.database.
try:
    from src.db import Base, get_db  # type: ignore[import]
except ModuleNotFoundError:
    try:
        from src.database import Base, get_db  # type: ignore[import]
    except ModuleNotFoundError:
        # Last resort: import from models and dependencies directly
        from src.models.base import Base  # type: ignore[import]
        from src.dependencies.database import get_db  # type: ignore[import]

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
    # Create device type and device without auth (API_KEY not set)
    monkeypatch.delenv("API_KEY", raising=False)
    dt_resp = client.post("/device-types/", json={"name": "TypeA"})
    assert dt_resp.status_code == 201
    dev_resp = client.post("/devices/", json={"serial_number": "SN-AUTH-1", "name": "Dev1", "device_type_id": dt_resp.json()["id"]})
    assert dev_resp.status_code == 201
    device_id = dev_resp.json()["id"]
    # Now set the key and try to delete without header
    monkeypatch.setenv("API_KEY", "secret")
    response = client.delete(f"/devices/{device_id}")
    assert response.status_code == 401


def test_put_device_wrong_key_returns_403(client, monkeypatch):
    """PUT /devices/{id} with API_KEY set but wrong header returns 403."""
    monkeypatch.delenv("API_KEY", raising=False)
    dt_resp = client.post("/device-types/", json={"name": "TypeB"})
    assert dt_resp.status_code == 201
    dev_resp = client.post("/devices/", json={"serial_number": "SN-AUTH-2", "name": "Dev2", "device_type_id": dt_resp.json()["id"]})
    assert dev_resp.status_code == 201
    device_id = dev_resp.json()["id"]
    monkeypatch.setenv("API_KEY", "secret")
    response = client.put(f"/devices/{device_id}", json={"name": "Updated"}, headers={"X-API-Key": "wrong"})
    assert response.status_code == 403
