"""Tests for the devices resource endpoints.

Covers CRUD operations and edge cases for the /devices API.
"""

from fastapi.testclient import TestClient


def _create_device_type(client: TestClient) -> int:
    """Helper to create a device type and return its ID.

    Args:
        client: The test client to use.

    Returns:
        The ID of the created device type.
    """
    response = client.post("/device-types/", json={"name": "TestType"})
    assert response.status_code == 201
    return response.json()["id"]


def test_create_device(client: TestClient) -> None:
    """Test creating a device returns 201 and correct body."""
    device_type_id = _create_device_type(client)
    response = client.post(
        "/devices/",
        json={"name": "Device A", "serial_number": "SN-001", "device_type_id": device_type_id},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Device A"
    assert body["serial_number"] == "SN-001"
    assert body["device_type_id"] == device_type_id
    assert "id" in body


def test_get_all_devices(client: TestClient) -> None:
    """Test retrieving all devices returns 200 and a list."""
    device_type_id = _create_device_type(client)
    client.post("/devices/", json={"name": "Device B", "device_type_id": device_type_id})
    response = client.get("/devices/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_get_device_by_id(client: TestClient) -> None:
    """Test retrieving a device by ID returns 200 and correct fields."""
    device_type_id = _create_device_type(client)
    create_resp = client.post(
        "/devices/", json={"name": "Device C", "device_type_id": device_type_id}
    )
    device_id = create_resp.json()["id"]
    response = client.get(f"/devices/{device_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == device_id
    assert body["name"] == "Device C"
    assert body["device_type_id"] == device_type_id


def test_get_device_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent device returns 404."""
    response = client.get("/devices/99999")
    assert response.status_code == 404


def test_create_device_invalid_device_type_id(client: TestClient) -> None:
    """Test creating a device with an invalid device_type_id returns 404."""
    response = client.post(
        "/devices/", json={"name": "Device D", "device_type_id": 99999}
    )
    assert response.status_code == 404


def test_update_device(client: TestClient) -> None:
    """Test updating a device returns 200 and the changed field."""
    device_type_id = _create_device_type(client)
    create_resp = client.post(
        "/devices/", json={"name": "Device E", "device_type_id": device_type_id}
    )
    device_id = create_resp.json()["id"]
    response = client.put(f"/devices/{device_id}", json={"name": "Device E Updated"})
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Device E Updated"
    assert body["id"] == device_id


def test_delete_device(client: TestClient) -> None:
    """Test deleting a device returns 204."""
    device_type_id = _create_device_type(client)
    create_resp = client.post(
        "/devices/", json={"name": "Device F", "device_type_id": device_type_id}
    )
    device_id = create_resp.json()["id"]
    response = client.delete(f"/devices/{device_id}")
    assert response.status_code == 204


def test_get_device_after_delete_returns_404(client: TestClient) -> None:
    """Test retrieving a deleted device returns 404."""
    device_type_id = _create_device_type(client)
    create_resp = client.post(
        "/devices/", json={"name": "Device G", "device_type_id": device_type_id}
    )
    device_id = create_resp.json()["id"]
    client.delete(f"/devices/{device_id}")
    response = client.get(f"/devices/{device_id}")
    assert response.status_code == 404
