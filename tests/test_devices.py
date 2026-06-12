"""Tests for the devices vertical slice."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.config.database import Base, get_db

SQLITE_URL = "sqlite:///:memory:"

_engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test and drop them after.

    Yields:
        None
    """
    Base.metadata.create_all(bind=_engine)

    def override_get_db():
        db = _TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=_engine)


@pytest.fixture()
def client():
    """Return a TestClient for the FastAPI app.

    Returns:
        TestClient instance.
    """
    return TestClient(app)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def create_device_type(client: TestClient, name: str = "Sensor") -> dict:
    """Pre-create a device type via the API and return its JSON body.

    Args:
        client: TestClient instance.
        name: Name for the device type.

    Returns:
        Parsed JSON response body of the created device type.
    """
    response = client.post("/device-types/", json={"name": name, "description": "test type"})
    assert response.status_code == 201, response.text
    return response.json()


def create_location(client: TestClient, name: str = "Warehouse A") -> dict:
    """Pre-create a location via the API and return its JSON body.

    Args:
        client: TestClient instance.
        name: Name for the location.

    Returns:
        Parsed JSON response body of the created location.
    """
    response = client.post("/locations/", json={"name": name, "description": "test location"})
    assert response.status_code == 201, response.text
    return response.json()


def make_device_payload(
    device_type_id: int,
    serial_number: str = "SN-001",
    location_id: int = None,
) -> dict:
    """Build a device creation payload.

    Args:
        device_type_id: ID of an existing device type.
        serial_number: Serial number string for the device.
        location_id: Optional location ID.

    Returns:
        Dictionary suitable for posting to POST /devices/.
    """
    payload = {
        "serial_number": serial_number,
        "name": "Test Device",
        "status": "active",
        "device_type_id": device_type_id,
    }
    if location_id is not None:
        payload["location_id"] = location_id
    return payload


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_create_device_returns_201_and_body(client):
    """POST /devices/ with valid data returns 201 and the created device body."""
    dt = create_device_type(client, "TypeA")
    payload = make_device_payload(dt["id"], serial_number="SN-CREATE-001")
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["serial_number"] == "SN-CREATE-001"
    assert body["name"] == "Test Device"
    assert body["status"] == "active"
    assert body["device_type_id"] == dt["id"]
    assert "id" in body
    assert "created_at" in body


def test_create_device_with_invalid_device_type_returns_422(client):
    """POST /devices/ with a non-existent device_type_id returns 422."""
    payload = make_device_payload(device_type_id=999999, serial_number="SN-INVALID-DT")
    response = client.post("/devices/", json=payload)
    assert response.status_code == 422, response.text
    assert "device_type" in response.json()["detail"]


def test_create_duplicate_serial_number_returns_400(client):
    """POST /devices/ with a duplicate serial_number returns 400."""
    dt = create_device_type(client, "TypeB")
    payload = make_device_payload(dt["id"], serial_number="SN-DUP-001")
    r1 = client.post("/devices/", json=payload)
    assert r1.status_code == 201, r1.text
    r2 = client.post("/devices/", json=payload)
    assert r2.status_code == 400, r2.text


def test_list_devices_returns_200(client):
    """GET /devices/ returns 200 and a list."""
    dt = create_device_type(client, "TypeC")
    payload = make_device_payload(dt["id"], serial_number="SN-LIST-001")
    client.post("/devices/", json=payload)
    response = client.get("/devices/")
    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_get_device_by_id_returns_200(client):
    """GET /devices/{id} returns 200 and the correct device."""
    dt = create_device_type(client, "TypeD")
    payload = make_device_payload(dt["id"], serial_number="SN-GET-001")
    created = client.post("/devices/", json=payload).json()
    response = client.get(f"/devices/{created['id']}")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["id"] == created["id"]
    assert body["serial_number"] == "SN-GET-001"


def test_get_device_missing_returns_404(client):
    """GET /devices/{id} for a non-existent device returns 404."""
    response = client.get("/devices/999999")
    assert response.status_code == 404, response.text


def test_update_device_returns_200_and_updated_fields(client):
    """PUT /devices/{id} returns 200 and the updated device fields."""
    dt = create_device_type(client, "TypeE")
    payload = make_device_payload(dt["id"], serial_number="SN-UPD-001")
    created = client.post("/devices/", json=payload).json()
    update_payload = {"name": "Updated Device", "status": "inactive"}
    response = client.put(f"/devices/{created['id']}", json=update_payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Updated Device"
    assert body["status"] == "inactive"
    assert body["serial_number"] == "SN-UPD-001"


def test_update_missing_device_returns_404(client):
    """PUT /devices/{id} for a non-existent device returns 404."""
    response = client.put("/devices/999999", json={"name": "Ghost"})
    assert response.status_code == 404, response.text


def test_delete_device_returns_204(client):
    """DELETE /devices/{id} returns 204 for an existing device."""
    dt = create_device_type(client, "TypeF")
    payload = make_device_payload(dt["id"], serial_number="SN-DEL-001")
    created = client.post("/devices/", json=payload).json()
    response = client.delete(f"/devices/{created['id']}")
    assert response.status_code == 204, response.text


def test_delete_missing_device_returns_404(client):
    """DELETE /devices/{id} for a non-existent device returns 404."""
    response = client.delete("/devices/999999")
    assert response.status_code == 404, response.text


def test_create_device_with_location_returns_201(client):
    """POST /devices/ with a valid location_id returns 201."""
    dt = create_device_type(client, "TypeG")
    loc = create_location(client, "Lab 1")
    payload = make_device_payload(
        dt["id"], serial_number="SN-LOC-001", location_id=loc["id"]
    )
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["location_id"] == loc["id"]


def test_create_device_with_invalid_location_returns_422(client):
    """POST /devices/ with a non-existent location_id returns 422."""
    dt = create_device_type(client, "TypeH")
    payload = make_device_payload(
        dt["id"], serial_number="SN-INVLOC-001", location_id=999999
    )
    response = client.post("/devices/", json=payload)
    assert response.status_code == 422, response.text
    assert "location" in response.json()["detail"]
