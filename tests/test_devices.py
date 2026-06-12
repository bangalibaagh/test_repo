"""Tests for the Device resource endpoints."""


def _create_device_type(client):
    """Helper to create a device type and return its ID.

    Args:
        client: The test client.

    Returns:
        The ID of the created device type.
    """
    resp = client.post("/device-types", json={"name": "Sensor", "description": "A sensor"})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_location(client):
    """Helper to create a location and return its ID.

    Args:
        client: The test client.

    Returns:
        The ID of the created location.
    """
    resp = client.post("/locations", json={"name": "Warehouse A", "description": "Main warehouse"})
    assert resp.status_code == 201
    return resp.json()["id"]


def test_create_device_returns_201_and_body(client):
    """Test that creating a device returns 201 and the correct fields.

    Args:
        client: The shared test client fixture.
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
    resp = client.post("/devices", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["serial_number"] == "SN-001"
    assert body["name"] == "Device One"
    assert body["device_type_id"] == dt_id
    assert body["location_id"] == loc_id
    assert body["status"] == "active"
    assert "id" in body


def test_list_devices_returns_200_and_list(client):
    """Test that listing devices returns 200 and a list.

    Args:
        client: The shared test client fixture.
    """
    dt_id = _create_device_type(client)
    client.post("/devices", json={"serial_number": "SN-002", "name": "Dev2", "device_type_id": dt_id})
    resp = client.get("/devices")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_get_device_by_id_returns_200(client):
    """Test that getting a device by ID returns 200 and the correct body.

    Args:
        client: The shared test client fixture.
    """
    dt_id = _create_device_type(client)
    create_resp = client.post("/devices", json={"serial_number": "SN-003", "name": "Dev3", "device_type_id": dt_id})
    device_id = create_resp.json()["id"]
    resp = client.get(f"/devices/{device_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == device_id


def test_update_device_returns_200_with_changed_fields(client):
    """Test that updating a device returns 200 and reflects the changes.

    Args:
        client: The shared test client fixture.
    """
    dt_id = _create_device_type(client)
    create_resp = client.post("/devices", json={"serial_number": "SN-004", "name": "Dev4", "device_type_id": dt_id})
    device_id = create_resp.json()["id"]
    resp = client.put(f"/devices/{device_id}", json={"name": "Updated Dev4"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Dev4"


def test_delete_device_returns_204(client):
    """Test that deleting a device returns 204.

    Args:
        client: The shared test client fixture.
    """
    dt_id = _create_device_type(client)
    create_resp = client.post("/devices", json={"serial_number": "SN-005", "name": "Dev5", "device_type_id": dt_id})
    device_id = create_resp.json()["id"]
    resp = client.delete(f"/devices/{device_id}")
    assert resp.status_code == 204


def test_get_device_after_delete_returns_404(client):
    """Test that getting a deleted device returns 404.

    Args:
        client: The shared test client fixture.
    """
    dt_id = _create_device_type(client)
    create_resp = client.post("/devices", json={"serial_number": "SN-006", "name": "Dev6", "device_type_id": dt_id})
    device_id = create_resp.json()["id"]
    client.delete(f"/devices/{device_id}")
    resp = client.get(f"/devices/{device_id}")
    assert resp.status_code == 404


def test_create_duplicate_serial_number_returns_409(client):
    """Test that creating a device with a duplicate serial number returns 409.

    Args:
        client: The shared test client fixture.
    """
    dt_id = _create_device_type(client)
    payload = {"serial_number": "SN-DUP", "name": "Dev Dup", "device_type_id": dt_id}
    resp1 = client.post("/devices", json=payload)
    assert resp1.status_code == 201
    resp2 = client.post("/devices", json={"serial_number": "SN-DUP", "name": "Dev Dup 2", "device_type_id": dt_id})
    assert resp2.status_code == 409


def test_create_device_invalid_device_type_returns_404(client):
    """Test that creating a device with a non-existent device_type_id returns 404.

    Args:
        client: The shared test client fixture.
    """
    payload = {"serial_number": "SN-NODT", "name": "No DT Device", "device_type_id": 99999}
    resp = client.post("/devices", json=payload)
    assert resp.status_code == 404


def test_create_device_invalid_location_returns_404(client):
    """Test that creating a device with a non-existent location_id returns 404.

    Args:
        client: The shared test client fixture.
    """
    dt_id = _create_device_type(client)
    payload = {
        "serial_number": "SN-NOLOC",
        "name": "No Loc Device",
        "device_type_id": dt_id,
        "location_id": 99999,
    }
    resp = client.post("/devices", json=payload)
    assert resp.status_code == 404


def test_get_missing_device_returns_404(client):
    """Test that getting a non-existent device returns 404.

    Args:
        client: The shared test client fixture.
    """
    resp = client.get("/devices/99999")
    assert resp.status_code == 404


def test_update_missing_device_returns_404(client):
    """Test that updating a non-existent device returns 404.

    Args:
        client: The shared test client fixture.
    """
    resp = client.put("/devices/99999", json={"name": "Ghost"})
    assert resp.status_code == 404


def test_delete_missing_device_returns_404(client):
    """Test that deleting a non-existent device returns 404.

    Args:
        client: The shared test client fixture.
    """
    resp = client.delete("/devices/99999")
    assert resp.status_code == 404
