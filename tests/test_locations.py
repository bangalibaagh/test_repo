"""Tests for the locations resource endpoints."""


def test_create_location(client):
    """Creating a location returns 201 and the created body."""
    response = client.post(
        "/locations/",
        json={"name": "HQ", "address": "123 Main St", "description": "Headquarters"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "HQ"
    assert data["address"] == "123 Main St"
    assert data["description"] == "Headquarters"
    assert "id" in data


def test_get_all_locations(client):
    """GET /locations/ returns 200 and a list."""
    client.post("/locations/", json={"name": "Site A"})
    response = client.get("/locations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_location_by_id(client):
    """GET /locations/{id} returns 200 and the correct fields."""
    created = client.post("/locations/", json={"name": "Site B", "address": "456 Elm St"}).json()
    location_id = created["id"]
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == location_id
    assert data["name"] == "Site B"
    assert data["address"] == "456 Elm St"


def test_get_location_not_found(client):
    """GET /locations/{id} returns 404 for a non-existent location."""
    response = client.get("/locations/99999")
    assert response.status_code == 404


def test_update_location(client):
    """PUT /locations/{id} returns 200 and the updated field."""
    created = client.post("/locations/", json={"name": "Old Name"}).json()
    location_id = created["id"]
    response = client.put(f"/locations/{location_id}", json={"name": "New Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"


def test_delete_location(client):
    """DELETE /locations/{id} returns 204."""
    created = client.post("/locations/", json={"name": "To Delete"}).json()
    location_id = created["id"]
    response = client.delete(f"/locations/{location_id}")
    assert response.status_code == 204


def test_get_location_after_delete(client):
    """GET /locations/{id} returns 404 after the location has been deleted."""
    created = client.post("/locations/", json={"name": "Gone"}).json()
    location_id = created["id"]
    client.delete(f"/locations/{location_id}")
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 404
