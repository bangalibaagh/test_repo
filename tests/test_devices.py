"""Tests for the devices resource endpoints."""


def _create_device_type(client):
    """Helper to create a device type and return its ID.

    Args:
        client: The TestClient instance.

    Returns:
        The integer ID of the created device type.
    """
    resp = client.post("/device-types/", json={"name": "Sensor", "description": "A sensor"})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_location(client):
    """Helper to create a location and return its ID.

    Args:
        client: The TestClient instance.

    Returns:
        The integer ID of the created location.
    """
    resp = client.post("/locations/", json={"name": "Warehouse A", "description": "Main warehouse"})
    assert resp.status_code == 201
    return resp.json()["id"]


def test_create_device_returns_201_and_body(client):
    """Test that creating a device with valid FK ids returns 201 and correct fields.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)
    loc_id = _create_location(client)

    resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-001",
            "name": "Device One",
            "device_type_id": dt_id,
            "location_id": loc_id,
            "status": "active",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["serial_number"] == "SN-001"
    assert body["name"] == "Device One"
    assert body["device_type_id"] == dt_id
    assert body["location_id"] == loc_id
    assert body["status"] == "active"
    assert "id" in body
    assert "created_at" in body


def test_create_device_invalid_device_type_returns_404(client):
    """Test that creating a device with an invalid device_type_id returns 404.

    Args:
        client: The TestClient fixture.
    """
    resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-002",
            "name": "Device Two",
            "device_type_id": 9999,
            "status": "active",
        },
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Device type not found"


def test_create_device_invalid_location_returns_404(client):
    """Test that creating a device with an invalid location_id returns 404.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)

    resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-003",
            "name": "Device Three",
            "device_type_id": dt_id,
            "location_id": 9999,
            "status": "active",
        },
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Location not found"


def test_create_duplicate_serial_number_returns_409(client):
    """Test that creating a device with a duplicate serial_number returns 409.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)

    client.post(
        "/devices/",
        json={
            "serial_number": "SN-DUP",
            "name": "Device Dup",
            "device_type_id": dt_id,
            "status": "active",
        },
    )
    resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-DUP",
            "name": "Device Dup 2",
            "device_type_id": dt_id,
            "status": "active",
        },
    )
    assert resp.status_code == 409
    assert resp.json()["detail"] == "Serial number already exists"


def test_list_devices_returns_200_and_list(client):
    """Test that listing devices returns 200 and a list.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)

    client.post(
        "/devices/",
        json={
            "serial_number": "SN-LIST",
            "name": "Device List",
            "device_type_id": dt_id,
            "status": "active",
        },
    )
    resp = client.get("/devices/")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_get_device_by_id_returns_200(client):
    """Test that getting a device by ID returns 200 and the correct device.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)

    create_resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-GET",
            "name": "Device Get",
            "device_type_id": dt_id,
            "status": "active",
        },
    )
    device_id = create_resp.json()["id"]

    resp = client.get(f"/devices/{device_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == device_id
    assert resp.json()["serial_number"] == "SN-GET"


def test_get_nonexistent_device_returns_404(client):
    """Test that getting a non-existent device returns 404.

    Args:
        client: The TestClient fixture.
    """
    resp = client.get("/devices/99999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Device not found"


def test_update_device_returns_200_with_changed_fields(client):
    """Test that updating a device returns 200 and the updated fields.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)

    create_resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-UPD",
            "name": "Device Update",
            "device_type_id": dt_id,
            "status": "active",
        },
    )
    device_id = create_resp.json()["id"]

    resp = client.put(
        f"/devices/{device_id}",
        json={"name": "Device Updated", "status": "inactive"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Device Updated"
    assert body["status"] == "inactive"


def test_delete_device_returns_204(client):
    """Test that deleting a device returns 204.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)

    create_resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-DEL",
            "name": "Device Delete",
            "device_type_id": dt_id,
            "status": "active",
        },
    )
    device_id = create_resp.json()["id"]

    resp = client.delete(f"/devices/{device_id}")
    assert resp.status_code == 204


def test_get_device_after_delete_returns_404(client):
    """Test that getting a deleted device returns 404.

    Args:
        client: The TestClient fixture.
    """
    dt_id = _create_device_type(client)

    create_resp = client.post(
        "/devices/",
        json={
            "serial_number": "SN-DELGET",
            "name": "Device DelGet",
            "device_type_id": dt_id,
            "status": "active",
        },
    )
    device_id = create_resp.json()["id"]

    client.delete(f"/devices/{device_id}")

    resp = client.get(f"/devices/{device_id}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Device not found"
