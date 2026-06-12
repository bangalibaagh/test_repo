"""Tests for the device_types vertical slice."""


def test_create_device_type_returns_201_and_body(client):
    """Test that creating a device type returns HTTP 201 and the correct JSON body.

    Args:
        client: The shared TestClient fixture.
    """
    payload = {"name": "Sensor", "description": "A sensor device type"}
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Sensor"
    assert body["description"] == "A sensor device type"
    assert "id" in body
    assert "created_at" in body


def test_list_device_types_returns_200_and_list(client):
    """Test that listing device types returns HTTP 200 and a list.

    Args:
        client: The shared TestClient fixture.
    """
    client.post("/device-types/", json={"name": "TypeA"})
    client.post("/device-types/", json={"name": "TypeB"})
    response = client.get("/device-types/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 2


def test_get_device_type_by_id_returns_200(client):
    """Test that retrieving a device type by ID returns HTTP 200 and correct data.

    Args:
        client: The shared TestClient fixture.
    """
    create_resp = client.post("/device-types/", json={"name": "Router"})
    device_type_id = create_resp.json()["id"]
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == device_type_id
    assert body["name"] == "Router"


def test_get_missing_device_type_returns_404(client):
    """Test that retrieving a non-existent device type returns HTTP 404.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.get("/device-types/99999")
    assert response.status_code == 404


def test_update_device_type_returns_200_with_changed_fields(client):
    """Test that updating a device type returns HTTP 200 with the updated fields.

    Args:
        client: The shared TestClient fixture.
    """
    create_resp = client.post("/device-types/", json={"name": "OldName"})
    device_type_id = create_resp.json()["id"]
    response = client.put(
        f"/device-types/{device_type_id}",
        json={"name": "NewName", "description": "Updated desc"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "NewName"
    assert body["description"] == "Updated desc"


def test_delete_device_type_returns_204(client):
    """Test that deleting an existing device type returns HTTP 204.

    Args:
        client: The shared TestClient fixture.
    """
    create_resp = client.post("/device-types/", json={"name": "ToDelete"})
    device_type_id = create_resp.json()["id"]
    response = client.delete(f"/device-types/{device_type_id}")
    assert response.status_code == 204


def test_delete_missing_device_type_returns_404(client):
    """Test that deleting a non-existent device type returns HTTP 404.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.delete("/device-types/99999")
    assert response.status_code == 404
