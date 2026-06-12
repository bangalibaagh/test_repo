"""Tests for the devices API endpoints."""


def _create_device_type(client):
    """Helper to create a device type and return its ID.

    Args:
        client: The FastAPI TestClient instance.

    Returns:
        int: The ID of the created device type.
    """
    response = client.post("/device-types/", json={"name": "Sensor", "description": "A sensor"})
    assert response.status_code == 201
    return response.json()["id"]


def _create_location(client):
    """Helper to create a location and return its ID.

    Args:
        client: The FastAPI TestClient instance.

    Returns:
        int: The ID of the created location.
    """
    response = client.post("/locations/", json={"name": "Warehouse A", "description": "Main warehouse"})
    assert response.status_code == 201
    return response.json()["id"]


def test_create_device_returns_201_and_body(client):
    """Test that POST /devices/ returns 201 and the created device body.

    Args:
        client: The FastAPI TestClient fixture.
    """
    dt_id = _create_device_type(client)
    loc_id = _create_location(client)
    payload = {
        "serial_number": "SN-001",
        "name": "Device One",
        "device_type_id": dt_id,
        "location_id": loc_id,
        "status": "active",
    }
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["serial_number"] == "SN-001"
    assert body["name"] == "Device One"
    assert body["device_type_id"] == dt_id
    assert body["location_id"] == loc_id
    assert body["status"] == "active"
    assert "id" in body
    assert "created_at" in body


def test_create_device_with_invalid_device_type_returns_404(client):
    """Test that POST /devices/ with a non-existent device_type_id returns 404.

    Args:
        client: The FastAPI TestClient fixture.
    """
    payload = {
        "serial_number": "SN-999",
        "name": "Ghost Device",
        "device_type_id": 9999,
        "status": "active",
    }
    response = client.post("/devices/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "DeviceType not found"


def test_create_device_with_invalid_location_returns_404(client):
    """Test that POST /devices/ with a non-existent location_id returns 404.

    Args:
        client: The FastAPI TestClient fixture.
    """
    dt_id = _create_device_type(client)
    payload = {
        "serial_number": "SN-888",
        "name": "Device Bad Loc",
        "device_type_id": dt_id,
        "location_id": 9999,
        "status": "active",
    }
    response = client.post("/devices/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"


def test_list_devices_returns_200_and_list(client):
    """Test that GET /devices/ returns 200 and a list containing created devices.

    Args:
        client: The FastAPI TestClient fixture.
    """
    dt_id = _create_device_type(client)
    client.post("/devices/", json={"serial_number": "SN-L1", "name": "D1", "device_type_id": dt_id})
    client.post("/devices/", json={"serial_number": "SN-L2", "name": "D2", "device_type_id": dt_id})
    response = client.get("/devices/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 2


def test_get_device_by_id_returns_200(client):
    """Test that GET /devices/{id} returns 200 and the correct device.

    Args:
        client: The FastAPI TestClient fixture.
    """
    dt_id = _create_device_type(client)
    create_resp = client.post(
        "/devices/", json={"serial_number": "SN-G1", "name": "GetMe", "device_type_id": dt_id}
    )
    device_id = create_resp.json()["id"]
    response = client.get(f"/devices/{device_id}")
    assert response.status_code == 200
    assert response.json()["id"] == device_id
    assert response.json()["serial_number"] == "SN-G1"


def test_get_missing_device_returns_404(client):
    """Test that GET /devices/{id} returns 404 for a non-existent device.

    Args:
        client: The FastAPI TestClient fixture.
    """
    response = client.get("/devices/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_update_device_returns_200_with_changed_fields(client):
    """Test that PUT /devices/{id} returns 200 and reflects updated fields.

    Args:
        client: The FastAPI TestClient fixture.
    """
    dt_id = _create_device_type(client)
    create_resp = client.post(
        "/devices/", json={"serial_number": "SN-U1", "name": "OldName", "device_type_id": dt_id}
    )
    device_id = create_resp.json()["id"]
    response = client.put(f"/devices/{device_id}", json={"name": "NewName", "status": "inactive"})
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "NewName"
    assert body["status"] == "inactive"


def test_delete_device_returns_204(client):
    """Test that DELETE /devices/{id} returns 204 for an existing device.

    Args:
        client: The FastAPI TestClient fixture.
    """
    dt_id = _create_device_type(client)
    create_resp = client.post(
        "/devices/", json={"serial_number": "SN-D1", "name": "DeleteMe", "device_type_id": dt_id}
    )
    device_id = create_resp.json()["id"]
    response = client.delete(f"/devices/{device_id}")
    assert response.status_code == 204


def test_delete_missing_device_returns_404(client):
    """Test that DELETE /devices/{id} returns 404 for a non-existent device.

    Args:
        client: The FastAPI TestClient fixture.
    """
    response = client.delete("/devices/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"
