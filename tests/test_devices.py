"""Tests for the devices vertical slice."""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def create_device_type(name: str = "Sensor") -> dict:
    """Pre-create a device type via the API and return its JSON body.

    Args:
        name: Name for the device type.

    Returns:
        Parsed JSON response body of the created device type.
    """
    response = client.post("/device-types/", json={"name": name, "description": "test type"})
    assert response.status_code == 201, response.text
    return response.json()


def create_location(name: str = "Warehouse A") -> dict:
    """Pre-create a location via the API and return its JSON body.

    Args:
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

def test_create_device_returns_201_and_body():
    """POST /devices/ with valid data returns 201 and the created device body."""
    dt = create_device_type("TypeA")
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


def test_create_device_with_invalid_device_type_returns_422():
    """POST /devices/ with a non-existent device_type_id returns 422."""
    payload = make_device_payload(device_type_id=999999, serial_number="SN-INVALID-DT")
    response = client.post("/devices/", json=payload)
    assert response.status_code == 422, response.text
    assert "device_type" in response.json()["detail"]


def test_create_device_with_invalid_location_returns_422():
    """POST /devices/ with a non-existent location_id returns 422."""
    dt = create_device_type("TypeForLocTest")
    payload = make_device_payload(
        device_type_id=dt["id"],
        serial_number="SN-INVALID-LOC",
        location_id=999999,
    )
    response = client.post("/devices/", json=payload)
    assert response.status_code == 422, response.text
    assert "location" in response.json()["detail"]


def test_create_duplicate_serial_number_returns_400():
    """POST /devices/ with a duplicate serial_number returns 400."""
    dt = create_device_type("TypeDup")
    payload = make_device_payload(dt["id"], serial_number="SN-DUP-001")
    r1 = client.post("/devices/", json=payload)
    assert r1.status_code == 201, r1.text
    r2 = client.post("/devices/", json=payload)
    assert r2.status_code == 400, r2.text


def test_list_devices_returns_200_and_list():
    """GET /devices/ returns 200 and a list."""
    response = client.get("/devices/")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


def test_get_device_by_id_returns_200():
    """GET /devices/{id} returns 200 and the correct device."""
    dt = create_device_type("TypeGet")
    payload = make_device_payload(dt["id"], serial_number="SN-GET-001")
    created = client.post("/devices/", json=payload).json()
    response = client.get(f"/devices/{created['id']}")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["id"] == created["id"]
    assert body["serial_number"] == "SN-GET-001"


def test_get_device_missing_returns_404():
    """GET /devices/{id} with a non-existent ID returns 404."""
    response = client.get("/devices/999999")
    assert response.status_code == 404, response.text


def test_update_device_returns_200_and_updated_fields():
    """PUT /devices/{id} returns 200 and the updated device."""
    dt = create_device_type("TypeUpd")
    payload = make_device_payload(dt["id"], serial_number="SN-UPD-001")
    created = client.post("/devices/", json=payload).json()
    update_payload = {"name": "Updated Device", "status": "inactive"}
    response = client.put(f"/devices/{created['id']}", json=update_payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Updated Device"
    assert body["status"] == "inactive"
    assert body["serial_number"] == "SN-UPD-001"


def test_update_device_with_invalid_device_type_returns_422():
    """PUT /devices/{id} with a non-existent device_type_id returns 422."""
    dt = create_device_type("TypeUpdInvalid")
    payload = make_device_payload(dt["id"], serial_number="SN-UPD-INVALID")
    created = client.post("/devices/", json=payload).json()
    response = client.put(f"/devices/{created['id']}", json={"device_type_id": 999999})
    assert response.status_code == 422, response.text
    assert "device_type" in response.json()["detail"]


def test_update_missing_device_returns_404():
    """PUT /devices/{id} with a non-existent ID returns 404."""
    response = client.put("/devices/999999", json={"name": "Ghost"})
    assert response.status_code == 404, response.text


def test_delete_device_returns_204():
    """DELETE /devices/{id} returns 204 for an existing device."""
    dt = create_device_type("TypeDel")
    payload = make_device_payload(dt["id"], serial_number="SN-DEL-001")
    created = client.post("/devices/", json=payload).json()
    response = client.delete(f"/devices/{created['id']}")
    assert response.status_code == 204, response.text
    # Confirm it's gone
    get_response = client.get(f"/devices/{created['id']}")
    assert get_response.status_code == 404


def test_delete_missing_device_returns_404():
    """DELETE /devices/{id} with a non-existent ID returns 404."""
    response = client.delete("/devices/999999")
    assert response.status_code == 404, response.text


def test_create_device_with_location_returns_201():
    """POST /devices/ with a valid location_id returns 201 and includes location_id."""
    dt = create_device_type("TypeWithLoc")
    loc = create_location("LocForDevice")
    payload = make_device_payload(
        dt["id"],
        serial_number="SN-LOC-001",
        location_id=loc["id"],
    )
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["location_id"] == loc["id"]
