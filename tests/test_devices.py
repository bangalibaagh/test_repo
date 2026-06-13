"""Tests for the /devices API endpoints."""


def _create_device_type(client, name="Sensor"):
    """Helper to create a device type and return its id."""
    response = client.post("/device-types/", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def _create_location(client, name="Lab"):
    """Helper to create a location and return its id."""
    response = client.post("/locations/", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def test_create_device_returns_201_with_correct_fields(client):
    """POST /devices/ should return 201 and the created device body."""
    dt_id = _create_device_type(client)
    payload = {
        "serial_number": "SN-001",
        "name": "Temperature Sensor",
        "device_type_id": dt_id,
        "status": "active",
    }
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["serial_number"] == "SN-001"
    assert data["name"] == "Temperature Sensor"
    assert data["device_type_id"] == dt_id
    assert data["status"] == "active"
    assert "id" in data
    assert "created_at" in data


def test_list_devices_returns_200_and_list(client):
    """GET /devices/ should return 200 and a list."""
    dt_id = _create_device_type(client, name="Router")
    client.post(
        "/devices/",
        json={"serial_number": "SN-002", "name": "Router A", "device_type_id": dt_id},
    )
    response = client.get("/devices/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_device_by_id_returns_200(client):
    """GET /devices/{id} should return 200 and the device."""
    dt_id = _create_device_type(client, name="Switch")
    create_resp = client.post(
        "/devices/",
        json={"serial_number": "SN-003", "name": "Switch B", "device_type_id": dt_id},
    )
    device_id = create_resp.json()["id"]
    response = client.get(f"/devices/{device_id}")
    assert response.status_code == 200
    assert response.json()["id"] == device_id


def test_get_device_nonexistent_returns_404(client):
    """GET /devices/{id} with unknown id should return 404."""
    response = client.get("/devices/99999")
    assert response.status_code == 404


def test_update_device_returns_200_with_changed_fields(client):
    """PUT /devices/{id} should return 200 and updated fields."""
    dt_id = _create_device_type(client, name="Hub")
    create_resp = client.post(
        "/devices/",
        json={"serial_number": "SN-004", "name": "Hub C", "device_type_id": dt_id},
    )
    device_id = create_resp.json()["id"]
    response = client.put(
        f"/devices/{device_id}", json={"name": "Hub C Updated", "status": "inactive"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Hub C Updated"
    assert data["status"] == "inactive"


def test_delete_device_returns_204(client):
    """DELETE /devices/{id} should return 204."""
    dt_id = _create_device_type(client, name="Gateway")
    create_resp = client.post(
        "/devices/",
        json={"serial_number": "SN-005", "name": "Gateway D", "device_type_id": dt_id},
    )
    device_id = create_resp.json()["id"]
    response = client.delete(f"/devices/{device_id}")
    assert response.status_code == 204


def test_delete_device_nonexistent_returns_404(client):
    """DELETE /devices/{id} with unknown id should return 404."""
    response = client.delete("/devices/99999")
    assert response.status_code == 404


def test_create_duplicate_serial_number_returns_409(client):
    """POST /devices/ with duplicate serial_number should return 409."""
    dt_id = _create_device_type(client, name="Repeater")
    payload = {"serial_number": "SN-DUP", "name": "Repeater E", "device_type_id": dt_id}
    client.post("/devices/", json=payload)
    response = client.post("/devices/", json=payload)
    assert response.status_code == 409


def test_create_device_invalid_device_type_returns_404(client):
    """POST /devices/ with non-existent device_type_id should return 404."""
    payload = {
        "serial_number": "SN-NODT",
        "name": "Ghost Device",
        "device_type_id": 99999,
    }
    response = client.post("/devices/", json=payload)
    assert response.status_code == 404


def test_create_device_with_location_returns_201(client):
    """POST /devices/ with a valid location_id should return 201."""
    dt_id = _create_device_type(client, name="Probe")
    loc_id = _create_location(client, name="Server Room")
    payload = {
        "serial_number": "SN-LOC",
        "name": "Probe F",
        "device_type_id": dt_id,
        "location_id": loc_id,
    }
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201
    assert response.json()["location_id"] == loc_id


def test_create_device_invalid_location_returns_404(client):
    """POST /devices/ with non-existent location_id should return 404."""
    dt_id = _create_device_type(client, name="Beacon")
    payload = {
        "serial_number": "SN-NOLOC",
        "name": "Beacon G",
        "device_type_id": dt_id,
        "location_id": 99999,
    }
    response = client.post("/devices/", json=payload)
    assert response.status_code == 404
