"""Tests for the devices vertical slice.

This module covers all CRUD endpoints exposed by the /devices router,
including error paths for duplicate serial numbers and invalid FK ids.
"""


def _create_device_type(client, name="TypeA"):
    """POST a device type and return the response JSON.

    Args:
        client: Starlette TestClient instance.
        name: Name for the device type.

    Returns:
        The parsed JSON body of the creation response.
    """
    resp = client.post("/device-types/", json={"name": name})
    return resp.json()


def _create_location(client, name="LocA"):
    """POST a location and return the response JSON.

    Args:
        client: Starlette TestClient instance.
        name: Name for the location.

    Returns:
        The parsed JSON body of the creation response.
    """
    resp = client.post("/locations/", json={"name": name})
    return resp.json()


def test_list_devices_empty(client):
    """GET /devices/ on an empty database should return 200 and an empty list.

    Args:
        client: Shared TestClient fixture.
    """
    resp = client.get("/devices/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_device_minimal(client):
    """POST /devices/ with only required fields should return 201 and the new record.

    Args:
        client: Shared TestClient fixture.
    """
    payload = {"serial_number": "SN-001", "name": "Device One"}
    resp = client.post("/devices/", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["serial_number"] == "SN-001"
    assert body["name"] == "Device One"
    assert body["status"] == "active"
    assert body["device_type_id"] is None
    assert body["location_id"] is None
    assert "id" in body
    assert "created_at" in body


def test_create_device_with_relations(client):
    """POST /devices/ with valid FK ids should return 201 and the linked record.

    Args:
        client: Shared TestClient fixture.
    """
    dt = _create_device_type(client, name="TypeB")
    loc = _create_location(client, name="LocB")
    payload = {
        "serial_number": "SN-002",
        "name": "Device Two",
        "device_type_id": dt["id"],
        "location_id": loc["id"],
    }
    resp = client.post("/devices/", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["device_type_id"] == dt["id"]
    assert body["location_id"] == loc["id"]


def test_create_device_duplicate_serial(client):
    """POST /devices/ with a duplicate serial_number should return 400.

    Args:
        client: Shared TestClient fixture.
    """
    payload = {"serial_number": "SN-DUP", "name": "Device Dup"}
    client.post("/devices/", json=payload)
    resp = client.post("/devices/", json=payload)
    assert resp.status_code == 400


def test_create_device_invalid_device_type(client):
    """POST /devices/ with a non-existent device_type_id should return 404.

    Args:
        client: Shared TestClient fixture.
    """
    payload = {"serial_number": "SN-003", "name": "Device Three", "device_type_id": 9999}
    resp = client.post("/devices/", json=payload)
    assert resp.status_code == 404


def test_create_device_invalid_location(client):
    """POST /devices/ with a non-existent location_id should return 404.

    Args:
        client: Shared TestClient fixture.
    """
    payload = {"serial_number": "SN-004", "name": "Device Four", "location_id": 9999}
    resp = client.post("/devices/", json=payload)
    assert resp.status_code == 404


def test_get_device(client):
    """GET /devices/{id} for an existing device should return 200 and the record.

    Args:
        client: Shared TestClient fixture.
    """
    created = client.post("/devices/", json={"serial_number": "SN-005", "name": "Device Five"}).json()
    resp = client.get(f"/devices/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["serial_number"] == "SN-005"


def test_get_device_not_found(client):
    """GET /devices/{id} for a missing device should return 404.

    Args:
        client: Shared TestClient fixture.
    """
    resp = client.get("/devices/99999")
    assert resp.status_code == 404


def test_update_device(client):
    """PUT /devices/{id} should update the specified fields and return 200.

    Args:
        client: Shared TestClient fixture.
    """
    created = client.post("/devices/", json={"serial_number": "SN-006", "name": "Device Six"}).json()
    resp = client.put(f"/devices/{created['id']}", json={"name": "Device Six Updated"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Device Six Updated"


def test_update_device_not_found(client):
    """PUT /devices/9999 should return 404 when the device does not exist.

    Args:
        client: Shared TestClient fixture.
    """
    resp = client.put("/devices/9999", json={"name": "Ghost Device"})
    assert resp.status_code == 404


def test_delete_device(client):
    """DELETE /devices/{id} should return 204 and subsequent GET should return 404.

    Args:
        client: Shared TestClient fixture.
    """
    created = client.post("/devices/", json={"serial_number": "SN-007", "name": "Device Seven"}).json()
    resp = client.delete(f"/devices/{created['id']}")
    assert resp.status_code == 204
    get_resp = client.get(f"/devices/{created['id']}")
    assert get_resp.status_code == 404


def test_delete_device_not_found(client):
    """DELETE /devices/9999 should return 404 when the device does not exist.

    Args:
        client: Shared TestClient fixture.
    """
    resp = client.delete("/devices/9999")
    assert resp.status_code == 404
