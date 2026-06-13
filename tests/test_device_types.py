"""Tests for the device-types resource endpoints.

Covers all five CRUD endpoints with status code and response body
assertions to achieve approximately 80% coverage of the resource slice.
"""

import pytest
from fastapi.testclient import TestClient


def test_list_device_types_empty(client: TestClient) -> None:
    """GET / returns 200 and an empty list when no device types exist."""
    response = client.get("/device-types/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_device_type(client: TestClient) -> None:
    """POST / returns 201 and the created device type body."""
    payload = {"name": "Sensor", "description": "A sensor device"}
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Sensor"
    assert body["description"] == "A sensor device"
    assert "id" in body


def test_create_device_type_duplicate_name(client: TestClient) -> None:
    """POST / with a duplicate name returns a non-201 error status."""
    payload = {"name": "Actuator"}
    client.post("/device-types/", json=payload)
    response = client.post("/device-types/", json=payload)
    assert response.status_code != 201


def test_list_device_types_contains_item(client: TestClient) -> None:
    """GET / returns 200 and a list containing the created item."""
    client.post("/device-types/", json={"name": "Gateway"})
    response = client.get("/device-types/")
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert "Gateway" in names


def test_get_device_type_by_id(client: TestClient) -> None:
    """GET /{id} returns 200 and the correct device type fields."""
    created = client.post(
        "/device-types/", json={"name": "Hub", "description": "Hub device"}
    ).json()
    device_type_id = created["id"]
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == device_type_id
    assert body["name"] == "Hub"
    assert body["description"] == "Hub device"


def test_get_device_type_not_found(client: TestClient) -> None:
    """GET /{id} returns 404 for a non-existent device type."""
    response = client.get("/device-types/99999")
    assert response.status_code == 404


def test_update_device_type(client: TestClient) -> None:
    """PUT /{id} returns 200 and the updated field value."""
    created = client.post("/device-types/", json={"name": "OldName"}).json()
    device_type_id = created["id"]
    response = client.put(f"/device-types/{device_type_id}", json={"name": "NewName"})
    assert response.status_code == 200
    assert response.json()["name"] == "NewName"


def test_update_device_type_not_found(client: TestClient) -> None:
    """PUT /{id} returns 404 for a non-existent device type."""
    response = client.put("/device-types/99999", json={"name": "X"})
    assert response.status_code == 404


def test_update_device_type_duplicate_name(client: TestClient) -> None:
    """PUT /{id} with a duplicate name returns a conflict error status."""
    client.post("/device-types/", json={"name": "TypeA"})
    created_b = client.post("/device-types/", json={"name": "TypeB"}).json()
    response = client.put(f"/device-types/{created_b['id']}", json={"name": "TypeA"})
    assert response.status_code == 409


def test_delete_device_type(client: TestClient) -> None:
    """DELETE /{id} returns 204 and the record is no longer accessible."""
    created = client.post("/device-types/", json={"name": "ToDelete"}).json()
    device_type_id = created["id"]
    response = client.delete(f"/device-types/{device_type_id}")
    assert response.status_code == 204


def test_get_after_delete_returns_404(client: TestClient) -> None:
    """GET /{id} returns 404 after the device type has been deleted."""
    created = client.post("/device-types/", json={"name": "Ephemeral"}).json()
    device_type_id = created["id"]
    client.delete(f"/device-types/{device_type_id}")
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 404


def test_delete_device_type_not_found(client: TestClient) -> None:
    """DELETE /{id} returns 404 for a non-existent device type."""
    response = client.delete("/device-types/99999")
    assert response.status_code == 404
