"""Integration tests exercising multiple resources together.

These tests verify cross-resource interactions such as creating a Device
that references both a DeviceType and a Location, and asserting correct
behaviour across the full lifecycle.
"""

import pytest


def test_full_device_lifecycle(client):
    """Test the full lifecycle of a Device referencing a DeviceType and Location.

    Creates a DeviceType and a Location, creates a Device referencing both,
    asserts the device fields match, updates the device status to 'inactive',
    asserts the update, deletes the device, and asserts a 404 is returned.

    Args:
        client: The shared TestClient fixture.
    """
    dt_resp = client.post("/device-types/", json={"name": "lifecycle-dt", "description": "desc"})
    assert dt_resp.status_code == 201
    device_type_id = dt_resp.json()["id"]

    loc_resp = client.post("/locations/", json={"name": "lifecycle-loc", "address": "123 St"})
    assert loc_resp.status_code == 201
    location_id = loc_resp.json()["id"]

    dev_payload = {
        "name": "lifecycle-dev",
        "serial_number": "SN-LIFECYCLE-001",
        "device_type_id": device_type_id,
        "location_id": location_id,
    }
    dev_resp = client.post("/devices/", json=dev_payload)
    assert dev_resp.status_code == 201, dev_resp.text
    device_id = dev_resp.json()["id"]
    assert dev_resp.json()["device_type_id"] == device_type_id
    assert dev_resp.json()["location_id"] == location_id

    get_resp = client.get(f"/devices/{device_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["device_type_id"] == device_type_id
    assert get_resp.json()["location_id"] == location_id

    current = get_resp.json()
    update_payload = {
        "name": current["name"],
        "serial_number": current["serial_number"],
        "device_type_id": device_type_id,
        "location_id": location_id,
    }
    if "status" in current:
        update_payload["status"] = "inactive"

    put_resp = client.put(f"/devices/{device_id}", json=update_payload)
    assert put_resp.status_code == 200, put_resp.text
    if "status" in put_resp.json():
        assert put_resp.json()["status"] == "inactive"

    del_resp = client.delete(f"/devices/{device_id}")
    assert del_resp.status_code == 204

    not_found_resp = client.get(f"/devices/{device_id}")
    assert not_found_resp.status_code == 404


def test_delete_device_type_does_not_cascade_error(client):
    """Test that deleting a DeviceType with an associated Device is handled gracefully.

    Creates a DeviceType and a Device referencing it, then attempts to delete
    the DeviceType. Asserts the response status is either 204 (cascade delete
    allowed) or 409 (FK constraint enforced), confirming the service handles
    both outcomes without an unhandled error.

    Args:
        client: The shared TestClient fixture.
    """
    dt_resp = client.post("/device-types/", json={"name": "cascade-dt", "description": "desc"})
    assert dt_resp.status_code == 201
    device_type_id = dt_resp.json()["id"]

    loc_resp = client.post("/locations/", json={"name": "cascade-loc", "address": "456 Ave"})
    assert loc_resp.status_code == 201
    location_id = loc_resp.json()["id"]

    dev_resp = client.post(
        "/devices/",
        json={
            "name": "cascade-dev",
            "serial_number": "SN-CASCADE-001",
            "device_type_id": device_type_id,
            "location_id": location_id,
        },
    )
    assert dev_resp.status_code == 201, dev_resp.text

    del_resp = client.delete(f"/device-types/{device_type_id}")
    assert del_resp.status_code in (204, 409), (
        f"Expected 204 or 409, got {del_resp.status_code}: {del_resp.text}"
    )


def test_list_all_resources_after_bulk_create(client):
    """Test that listing resources returns at least the bulk-created items.

    Creates 3 DeviceTypes, 3 Locations, and 3 Devices, then asserts that
    GET /device-types/, GET /locations/, and GET /devices/ each return at
    least 3 items.

    Args:
        client: The shared TestClient fixture.
    """
    dt_ids = []
    for i in range(3):
        resp = client.post(
            "/device-types/",
            json={"name": f"bulk-dt-{i}", "description": f"desc-{i}"},
        )
        assert resp.status_code == 201, resp.text
        dt_ids.append(resp.json()["id"])

    loc_ids = []
    for i in range(3):
        resp = client.post(
            "/locations/",
            json={"name": f"bulk-loc-{i}", "address": f"{i} Bulk St"},
        )
        assert resp.status_code == 201, resp.text
        loc_ids.append(resp.json()["id"])

    for i in range(3):
        resp = client.post(
            "/devices/",
            json={
                "name": f"bulk-dev-{i}",
                "serial_number": f"SN-BULK-{i:03d}",
                "device_type_id": dt_ids[i],
                "location_id": loc_ids[i],
            },
        )
        assert resp.status_code == 201, resp.text

    dt_list_resp = client.get("/device-types/")
    assert dt_list_resp.status_code == 200
    assert len(dt_list_resp.json()) >= 3

    loc_list_resp = client.get("/locations/")
    assert loc_list_resp.status_code == 200
    assert len(loc_list_resp.json()) >= 3

    dev_list_resp = client.get("/devices/")
    assert dev_list_resp.status_code == 200
    assert len(dev_list_resp.json()) >= 3


def test_update_device_reassign_location(client):
    """Test that a Device can be reassigned to a different Location.

    Creates two Locations and a Device at the first Location, then PUTs
    the Device with the second Location's ID and asserts the location_id
    is updated correctly.

    Args:
        client: The shared TestClient fixture.
    """
    dt_resp = client.post("/device-types/", json={"name": "reassign-dt", "description": "desc"})
    assert dt_resp.status_code == 201
    device_type_id = dt_resp.json()["id"]

    loc1_resp = client.post("/locations/", json={"name": "reassign-loc-1", "address": "1 First St"})
    assert loc1_resp.status_code == 201
    location_id_1 = loc1_resp.json()["id"]

    loc2_resp = client.post("/locations/", json={"name": "reassign-loc-2", "address": "2 Second St"})
    assert loc2_resp.status_code == 201
    location_id_2 = loc2_resp.json()["id"]

    dev_resp = client.post(
        "/devices/",
        json={
            "name": "reassign-dev",
            "serial_number": "SN-REASSIGN-001",
            "device_type_id": device_type_id,
            "location_id": location_id_1,
        },
    )
    assert dev_resp.status_code == 201, dev_resp.text
    device_id = dev_resp.json()["id"]
    assert dev_resp.json()["location_id"] == location_id_1

    current = dev_resp.json()
    update_payload = {
        "name": current["name"],
        "serial_number": current["serial_number"],
        "device_type_id": device_type_id,
        "location_id": location_id_2,
    }
    if "status" in current:
        update_payload["status"] = current["status"]

    put_resp = client.put(f"/devices/{device_id}", json=update_payload)
    assert put_resp.status_code == 200, put_resp.text
    assert put_resp.json()["location_id"] == location_id_2


def test_health_still_ok(client):
    """Regression guard: assert the health endpoint still returns 200.

    Args:
        client: The shared TestClient fixture.
    """
    resp = client.get("/health")
    assert resp.status_code == 200
