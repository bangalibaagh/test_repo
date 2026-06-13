"""Tests for the Location API endpoints.

This module contains integration tests for all location CRUD endpoints
using the shared ``client`` fixture.
"""


def test_list_locations_empty(client):
    """Test that listing locations returns an empty list when none exist.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.get("/locations/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_location(client):
    """Test that a location can be created successfully.

    Args:
        client: The shared TestClient fixture.
    """
    payload = {"name": "Warehouse A", "address": "123 Main St"}
    response = client.post("/locations/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["name"] == "Warehouse A"


def test_create_location_duplicate_name(client):
    """Test that creating a location with a duplicate name returns 400.

    Args:
        client: The shared TestClient fixture.
    """
    payload = {"name": "Warehouse B"}
    client.post("/locations/", json=payload)
    response = client.post("/locations/", json=payload)
    assert response.status_code == 400


def test_get_location(client):
    """Test that a created location can be retrieved by id.

    Args:
        client: The shared TestClient fixture.
    """
    create_response = client.post("/locations/", json={"name": "Site C"})
    location_id = create_response.json()["id"]
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Site C"


def test_get_location_not_found(client):
    """Test that retrieving a non-existent location returns 404.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.get("/locations/99999")
    assert response.status_code == 404


def test_update_location(client):
    """Test that a location can be updated successfully.

    Args:
        client: The shared TestClient fixture.
    """
    create_response = client.post("/locations/", json={"name": "Old Name"})
    location_id = create_response.json()["id"]
    response = client.put(f"/locations/{location_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_update_location_not_found(client):
    """Test that updating a non-existent location returns 404.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.put("/locations/9999", json={"name": "Ghost Location"})
    assert response.status_code == 404


def test_update_location_duplicate_name(client):
    """Test that renaming a location to an already-used name returns 400.

    Args:
        client: The shared TestClient fixture.
    """
    client.post("/locations/", json={"name": "LocAlpha"})
    second = client.post("/locations/", json={"name": "LocBeta"})
    second_id = second.json()["id"]
    response = client.put(f"/locations/{second_id}", json={"name": "LocAlpha"})
    assert response.status_code == 400


def test_delete_location(client):
    """Test that a location can be deleted successfully.

    Args:
        client: The shared TestClient fixture.
    """
    create_response = client.post("/locations/", json={"name": "To Delete"})
    location_id = create_response.json()["id"]
    response = client.delete(f"/locations/{location_id}")
    assert response.status_code == 204
    get_response = client.get(f"/locations/{location_id}")
    assert get_response.status_code == 404


def test_delete_location_not_found(client):
    """Test that deleting a non-existent location returns 404.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.delete("/locations/9999")
    assert response.status_code == 404
