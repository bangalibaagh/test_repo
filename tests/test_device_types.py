"""Tests for the device_types API endpoints."""


def test_create_device_type_returns_201_and_body(client):
    """Creating a device type returns 201 and the correct fields."""
    payload = {"name": "Sensor", "description": "A sensor device"}
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Sensor"
    assert body["description"] == "A sensor device"
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_list_device_types_returns_200_and_list(client):
    """Listing device types returns 200 and a list."""
    client.post("/device-types/", json={"name": "TypeA"})
    client.post("/device-types/", json={"name": "TypeB"})
    response = client.get("/device-types/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 2


def test_get_device_type_by_id_returns_200(client):
    """Getting a device type by ID returns 200 and the correct record."""
    create_resp = client.post("/device-types/", json={"name": "Router"})
    device_type_id = create_resp.json()["id"]
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 200
    assert response.json()["id"] == device_type_id
    assert response.json()["name"] == "Router"


def test_get_missing_device_type_returns_404(client):
    """Getting a non-existent device type returns 404."""
    response = client.get("/device-types/99999")
    assert response.status_code == 404


def test_update_device_type_returns_200_with_changed_fields(client):
    """Updating a device type returns 200 and the updated fields."""
    create_resp = client.post("/device-types/", json={"name": "Switch", "description": "Old desc"})
    device_type_id = create_resp.json()["id"]
    update_payload = {"description": "New desc"}
    response = client.put(f"/device-types/{device_type_id}", json=update_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "New desc"
    assert body["name"] == "Switch"


def test_delete_device_type_returns_204(client):
    """Deleting a device type returns 204."""
    create_resp = client.post("/device-types/", json={"name": "Hub"})
    device_type_id = create_resp.json()["id"]
    response = client.delete(f"/device-types/{device_type_id}")
    assert response.status_code == 204


def test_delete_missing_device_type_returns_404(client):
    """Deleting a non-existent device type returns 404."""
    response = client.delete("/device-types/99999")
    assert response.status_code == 404


def test_get_device_type_after_delete_returns_404(client):
    """Getting a device type after deletion returns 404."""
    create_resp = client.post("/device-types/", json={"name": "Bridge"})
    device_type_id = create_resp.json()["id"]
    client.delete(f"/device-types/{device_type_id}")
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 404
