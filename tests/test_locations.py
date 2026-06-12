"""Tests for the locations API endpoints."""


def test_create_location_returns_201(client):
    """POST /locations/ should create a location and return 201 with JSON body.

    Args:
        client: Shared TestClient fixture backed by an in-memory database.
    """
    payload = {"name": "Warehouse A", "address": "1 Main St", "latitude": 51.5, "longitude": -0.1}
    response = client.post("/locations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Warehouse A"
    assert data["address"] == "1 Main St"
    assert data["latitude"] == 51.5
    assert data["longitude"] == -0.1
    assert "created_at" in data


def test_list_locations_returns_200(client):
    """GET /locations/ should return 200 and a list containing created locations.

    Args:
        client: Shared TestClient fixture backed by an in-memory database.
    """
    client.post("/locations/", json={"name": "Site 1"})
    client.post("/locations/", json={"name": "Site 2"})
    response = client.get("/locations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_location_returns_200(client):
    """GET /locations/{id} should return 200 and the correct location.

    Args:
        client: Shared TestClient fixture backed by an in-memory database.
    """
    created = client.post("/locations/", json={"name": "Depot"}).json()
    response = client.get(f"/locations/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Depot"


def test_get_missing_location_returns_404(client):
    """GET /locations/{id} with a non-existent id should return 404.

    Args:
        client: Shared TestClient fixture backed by an in-memory database.
    """
    response = client.get("/locations/99999")
    assert response.status_code == 404


def test_update_location_returns_200(client):
    """PUT /locations/{id} should update the location and return 200.

    Args:
        client: Shared TestClient fixture backed by an in-memory database.
    """
    created = client.post("/locations/", json={"name": "Old Name"}).json()
    response = client.put(f"/locations/{created['id']}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_location_returns_204(client):
    """DELETE /locations/{id} should delete the location and return 204.

    Args:
        client: Shared TestClient fixture backed by an in-memory database.
    """
    created = client.post("/locations/", json={"name": "To Delete"}).json()
    response = client.delete(f"/locations/{created['id']}")
    assert response.status_code == 204


def test_delete_missing_location_returns_404(client):
    """DELETE /locations/{id} with a non-existent id should return 404.

    Args:
        client: Shared TestClient fixture backed by an in-memory database.
    """
    response = client.delete("/locations/99999")
    assert response.status_code == 404
