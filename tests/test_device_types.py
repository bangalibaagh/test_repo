"""Tests for the device_types vertical slice."""


def test_create_device_type_returns_201_and_body(client):
    """Test that creating a device type returns 201 and correct JSON fields.

    Args:
        client: The shared test HTTP client fixture.
    """
    response = client.post("/device-types/", json={"name": "Sensor", "description": "A sensor device"})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Sensor"
    assert body["description"] == "A sensor device"
    assert "id" in body
    assert "created_at" in body


def test_list_device_types_returns_200_and_list(client):
    """Test that listing device types returns 200 and a list containing created items.

    Args:
        client: The shared test HTTP client fixture.
    """
    client.post("/device-types/", json={"name": "Router", "description": "A router"})
    response = client.get("/device-types/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    names = [item["name"] for item in body]
    assert "Router" in names


def test_get_device_type_by_id_returns_200(client):
    """Test that getting a device type by ID returns 200 and correct data.

    Args:
        client: The shared test HTTP client fixture.
    """
    create_response = client.post("/device-types/", json={"name": "Switch", "description": "A switch"})
    device_type_id = create_response.json()["id"]
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == device_type_id
    assert body["name"] == "Switch"


def test_get_missing_device_type_returns_404(client):
    """Test that getting a non-existent device type returns 404.

    Args:
        client: The shared test HTTP client fixture.
    """
    response = client.get("/device-types/99999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_create_duplicate_device_type_returns_409(client):
    """Test that creating a device type with a duplicate name returns 409.

    Args:
        client: The shared test HTTP client fixture.
    """
    client.post("/device-types/", json={"name": "Hub", "description": "A hub"})
    response = client.post("/device-types/", json={"name": "Hub", "description": "Another hub"})
    assert response.status_code == 409
    assert "detail" in response.json()


def test_update_device_type_returns_200_with_changed_fields(client):
    """Test that updating a device type returns 200 and the changed field.

    Args:
        client: The shared test HTTP client fixture.
    """
    create_response = client.post("/device-types/", json={"name": "Gateway", "description": "Old desc"})
    device_type_id = create_response.json()["id"]
    response = client.put(f"/device-types/{device_type_id}", json={"description": "New desc"})
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "New desc"
    assert body["name"] == "Gateway"


def test_delete_device_type_returns_204(client):
    """Test that deleting a device type returns 204 with no body.

    Args:
        client: The shared test HTTP client fixture.
    """
    create_response = client.post("/device-types/", json={"name": "Bridge", "description": "A bridge"})
    device_type_id = create_response.json()["id"]
    response = client.delete(f"/device-types/{device_type_id}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_device_type_returns_404(client):
    """Test that deleting a non-existent device type returns 404.

    Args:
        client: The shared test HTTP client fixture.
    """
    response = client.delete("/device-types/99999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_device_type_after_delete_returns_404(client):
    """Test that getting a device type after deletion returns 404.

    Args:
        client: The shared test HTTP client fixture.
    """
    create_response = client.post("/device-types/", json={"name": "Repeater", "description": "A repeater"})
    device_type_id = create_response.json()["id"]
    client.delete(f"/device-types/{device_type_id}")
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 404
    assert "detail" in response.json()
