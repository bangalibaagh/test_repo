"""Tests for the device_types API endpoints.

This module covers CRUD operations for device types using the shared
client fixture.
"""


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
    assert "updated_at" in data


def test_get_device_type_by_id_returns_200(client):
    """GET /{id} returns 200 and the correct device type."""
    create_response = client.post("/device-types/", json={"name": "Actuator"})
    device_type_id = create_response.json()["id"]

    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Actuator"


def test_get_device_type_nonexistent_returns_404(client):
    """GET /{id} returns 404 when the device type does not exist."""
    response = client.get("/device-types/99999")
    assert response.status_code == 404


def test_update_device_type_returns_200_with_changed_fields(client):
    """PUT /{id} returns 200 and the updated device type fields."""
    create_response = client.post("/device-types/", json={"name": "Gateway"})
    device_type_id = create_response.json()["id"]

    update_payload = {"name": "Updated Gateway", "description": "Updated desc"}
    response = client.put(f"/device-types/{device_type_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Gateway"
    assert data["description"] == "Updated desc"


def test_update_device_type_nonexistent_returns_404(client):
    """PUT /{id} returns 404 when the device type does not exist."""
    response = client.put("/device-types/99999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_device_type_returns_204(client):
    """DELETE /{id} returns 204 when the device type is successfully deleted."""
    create_response = client.post("/device-types/", json={"name": "ToDelete"})
    device_type_id = create_response.json()["id"]

    response = client.delete(f"/device-types/{device_type_id}")
    assert response.status_code == 204


def test_delete_device_type_nonexistent_returns_404(client):
    """DELETE /{id} returns 404 when the device type does not exist."""
    response = client.delete("/device-types/99999")
    assert response.status_code == 404
