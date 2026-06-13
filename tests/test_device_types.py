"""Tests for the device_types resource slice."""

import pytest


def test_list_device_types_returns_200_and_empty_list(client):
    """GET / returns 200 and an empty list when no device types exist."""
    response = client.get("/device-types/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_device_type_returns_201_with_correct_fields(client):
    """POST / returns 201 and the created device type with correct fields."""
    payload = {"name": "Sensor", "description": "A sensor device"}
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sensor"
    assert data["description"] == "A sensor device"
    assert "id" in data
    assert "created_at" in data


def test_get_device_type_by_id_returns_200(client):
    """GET /{id} returns 200 and the correct device type."""
    create_resp = client.post("/device-types/", json={"name": "Actuator", "description": None})
    assert create_resp.status_code == 201
    created_id = create_resp.json()["id"]

    response = client.get(f"/device-types/{created_id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_id
    assert response.json()["name"] == "Actuator"


def test_get_device_type_nonexistent_returns_404(client):
    """GET /{id} returns 404 when the device type does not exist."""
    response = client.get("/device-types/99999")
    assert response.status_code == 404


def test_update_device_type_returns_200_with_changed_fields(client):
    """PUT /{id} returns 200 and the updated device type."""
    create_resp = client.post("/device-types/", json={"name": "Gateway", "description": "Old desc"})
    assert create_resp.status_code == 201
    created_id = create_resp.json()["id"]

    update_resp = client.put(f"/device-types/{created_id}", json={"description": "New desc"})
    assert update_resp.status_code == 200
    assert update_resp.json()["description"] == "New desc"
    assert update_resp.json()["name"] == "Gateway"


def test_update_device_type_nonexistent_returns_404(client):
    """PUT /{id} returns 404 when the device type does not exist."""
    response = client.put("/device-types/99999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_device_type_returns_204(client):
    """DELETE /{id} returns 204 when the device type is deleted."""
    create_resp = client.post("/device-types/", json={"name": "ToDelete", "description": None})
    assert create_resp.status_code == 201
    created_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/device-types/{created_id}")
    assert delete_resp.status_code == 204


def test_delete_device_type_nonexistent_returns_404(client):
    """DELETE /{id} returns 404 when the device type does not exist."""
    response = client.delete("/device-types/99999")
    assert response.status_code == 404


def test_create_duplicate_device_type_returns_409(client):
    """POST / returns 409 when a device type with the same name already exists."""
    payload = {"name": "Duplicate", "description": None}
    first_resp = client.post("/device-types/", json=payload)
    assert first_resp.status_code == 201

    second_resp = client.post("/device-types/", json=payload)
    assert second_resp.status_code == 409
