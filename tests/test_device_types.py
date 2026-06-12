"""Tests for the device_types vertical slice (routes, service, model)."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.main import app

SQLITE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLITE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=False)
def client():
    """Provide a TestClient with an isolated in-memory SQLite database."""
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_create_device_type_returns_201_and_body(client):
    """POST / should return 201 and the created device type body."""
    payload = {"name": "Sensor", "description": "A sensor device"}
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Sensor"
    assert body["description"] == "A sensor device"
    assert "id" in body
    assert "created_at" in body


def test_create_duplicate_name_returns_400(client):
    """POST / with a duplicate name should return 400."""
    payload = {"name": "Actuator"}
    client.post("/device-types/", json=payload)
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 400


def test_list_device_types_returns_200_and_list(client):
    """GET / should return 200 and a list of device types."""
    client.post("/device-types/", json={"name": "TypeA"})
    client.post("/device-types/", json={"name": "TypeB"})
    response = client.get("/device-types/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 2
    names = [item["name"] for item in body]
    assert "TypeA" in names
    assert "TypeB" in names


def test_get_device_type_by_id_returns_200(client):
    """GET /{id} should return 200 and the correct device type."""
    created = client.post("/device-types/", json={"name": "Camera"}).json()
    device_type_id = created["id"]
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == device_type_id
    assert body["name"] == "Camera"


def test_get_device_type_missing_returns_404(client):
    """GET /{id} for a non-existent id should return 404."""
    response = client.get("/device-types/99999")
    assert response.status_code == 404


def test_update_device_type_returns_200_and_updated_fields(client):
    """PUT /{id} should return 200 and the updated device type."""
    created = client.post("/device-types/", json={"name": "OldName"}).json()
    device_type_id = created["id"]
    response = client.put(
        f"/device-types/{device_type_id}",
        json={"name": "NewName", "description": "Updated desc"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "NewName"
    assert body["description"] == "Updated desc"


def test_update_missing_device_type_returns_404(client):
    """PUT /{id} for a non-existent id should return 404."""
    response = client.put("/device-types/99999", json={"name": "X"})
    assert response.status_code == 404


def test_delete_device_type_returns_204(client):
    """DELETE /{id} should return 204 for an existing device type."""
    created = client.post("/device-types/", json={"name": "ToDelete"}).json()
    device_type_id = created["id"]
    response = client.delete(f"/device-types/{device_type_id}")
    assert response.status_code == 204


def test_delete_missing_device_type_returns_404(client):
    """DELETE /{id} for a non-existent id should return 404."""
    response = client.delete("/device-types/99999")
    assert response.status_code == 404


def test_deleted_device_type_no_longer_accessible(client):
    """After DELETE, GET /{id} should return 404."""
    created = client.post("/device-types/", json={"name": "Ephemeral"}).json()
    device_type_id = created["id"]
    client.delete(f"/device-types/{device_type_id}")
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 404
