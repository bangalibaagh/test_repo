"""Integration tests exercising multiple resources together.

These tests verify cross-resource interactions such as creating a Device
that references both a DeviceType and a Location, and asserting correct
behaviour across the full lifecycle.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI application.

    Yields:
        TestClient: A test client bound to the FastAPI app.
    """
    with TestClient(app) as c:
        yield c


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

    dev_resp = client.post("/devices/", json={
        "name": "lifecycle-dev",
        "device_type_id": device_type_id,
        "location_id": location_id,
        "status": "active",
    })
    assert dev_resp.status_code == 201
    device_id = dev_resp.json()["id"]
    assert dev_resp.json()["device_type_id"] == device_type_id
    assert dev_resp.json()["location_id"] == location_id

    get_resp = client.get(f"/devices/{device_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["device_type_id"] == device_type_id
    assert get_resp.json()["location_id"] == location_id

    put_resp = client.put(f"/devices/{device_id}", json={
        "name": "lifecycle-dev",
        "device_type_id": device_type_id,
        "location_id": location_id,
        "status": "inactive",
    })
    assert put_resp.status_code == 200
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

    dev_resp = client.post("/devices/", json={
        "name": "cascade-dev",
        "device_type_id": device_type_id,
        "location_id": location_id,
        "status": "active",
    })
    assert dev_resp.status_code == 201

    del_resp = client.delete(f"/device-types/{device_type_id}")
    assert del_resp.status_code in (204, 409)


def test_list_all_resources_after_bulk_create(client):
    """Test that listing endpoints return at least the bulk-created resources.

    Creates 3 DeviceTypes, 3 Locations, and 3 Devices, then asserts that
    GET /device-types/, GET /locations/, and GET /devices/ each return at
    least 3 items.

    Args:
        client: The shared TestClient fixture.
    """
    loc_ids = []
    for i in range(3):
        loc_resp = client.post("/locations/", json={"name": f"bulk-loc-{i}", "address": f"{i} Rd"})
        assert loc_resp.status_code == 201
        loc_ids.append(loc_resp.json()["id"])

    dt_ids = []
    for i in range(3):
        dt_resp = client.post("/device-types/", json={"name": f"bulk-dt-{i}", "description": "d"})
        assert dt_resp.status_code == 201
        dt_ids.append(dt_resp.json()["id"])

    for i in range(3):
        dev_resp = client.post("/devices/", json={
            "name": f"bulk-dev-{i}",
            "device_type_id": dt_ids[i],
            "location_id": loc_ids[i],
            "status": "active",
        })
        assert dev_resp.status_code == 201

    dt_list = client.get("/device-types/")
    assert dt_list.status_code == 200
    assert len(dt_list.json()) >= 3

    loc_list = client.get("/locations/")
    assert loc_list.status_code == 200
    assert len(loc_list.json()) >= 3

    dev_list = client.get("/devices/")
    assert dev_list.status_code == 200
    assert len(dev_list.json()) >= 3


def test_update_device_reassign_location(client):
    """Test that a Device can be reassigned to a different Location via PUT.

    Creates two Locations and a Device at the first Location, then updates
    the Device to reference the second Location and asserts the location_id
    is updated correctly.

    Args:
        client: The shared TestClient fixture.
    """
    loc1_resp = client.post("/locations/", json={"name": "reassign-loc-1", "address": "1 Way"})
    assert loc1_resp.status_code == 201
    location_id_1 = loc1_resp.json()["id"]

    loc2_resp = client.post("/locations/", json={"name": "reassign-loc-2", "address": "2 Way"})
    assert loc2_resp.status_code == 201
    location_id_2 = loc2_resp.json()["id"]

    dt_resp = client.post("/device-types/", json={"name": "reassign-dt", "description": "d"})
    assert dt_resp.status_code == 201
    device_type_id = dt_resp.json()["id"]

    dev_resp = client.post("/devices/", json={
        "name": "reassign-dev",
        "device_type_id": device_type_id,
        "location_id": location_id_1,
        "status": "active",
    })
    assert dev_resp.status_code == 201
    device_id = dev_resp.json()["id"]
    assert dev_resp.json()["location_id"] == location_id_1

    put_resp = client.put(f"/devices/{device_id}", json={
        "name": "reassign-dev",
        "device_type_id": device_type_id,
        "location_id": location_id_2,
        "status": "active",
    })
    assert put_resp.status_code == 200
    assert put_resp.json()["location_id"] == location_id_2


def test_health_still_ok(client):
    """Regression guard: assert the health endpoint returns 200.

    Args:
        client: The shared TestClient fixture.
    """
    resp = client.get("/health")
    assert resp.status_code == 200
