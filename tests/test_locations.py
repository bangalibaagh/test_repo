"""Tests for the locations resource endpoints."""


def test_create_location(client):
    """Test creating a location returns 201 and correct fields.

    Args:
        client: Shared test HTTP client fixture.
    """
    payload = {"name": "HQ", "address": "123 Main St", "latitude": 1.23, "longitude": 4.56}
    response = client.post("/locations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "HQ"
    assert data["address"] == "123 Main St"
    assert data["latitude"] == 1.23
    assert data["longitude"] == 4.56
    assert "id" in data
    assert "created_at" in data


def test_list_locations(client):
    """Test listing locations returns 200 and includes created item.

    Args:
        client: Shared test HTTP client fixture.
    """
    client.post("/locations/", json={"name": "Warehouse"})
    response = client.get("/locations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    names = [item["name"] for item in data]
    assert "Warehouse" in names


def test_get_location_by_id(client):
    """Test retrieving a location by id returns 200 and correct data.

    Args:
        client: Shared test HTTP client fixture.
    """
    created = client.post("/locations/", json={"name": "Depot"}).json()
    location_id = created["id"]
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == location_id
    assert data["name"] == "Depot"


def test_get_nonexistent_location(client):
    """Test retrieving a non-existent location returns 404.

    Args:
        client: Shared test HTTP client fixture.
    """
    response = client.get("/locations/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"


def test_duplicate_location_name(client):
    """Test creating a location with a duplicate name returns 409.

    Args:
        client: Shared test HTTP client fixture.
    """
    client.post("/locations/", json={"name": "Unique"})
    response = client.post("/locations/", json={"name": "Unique"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Location name already exists"


def test_update_location(client):
    """Test updating a location returns 200 and the changed field.

    Args:
        client: Shared test HTTP client fixture.
    """
    created = client.post("/locations/", json={"name": "OldName"}).json()
    location_id = created["id"]
    response = client.put(f"/locations/{location_id}", json={"name": "NewName"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == location_id
    assert data["name"] == "NewName"


def test_delete_location(client):
    """Test deleting a location returns 204.

    Args:
        client: Shared test HTTP client fixture.
    """
    created = client.post("/locations/", json={"name": "ToDelete"}).json()
    location_id = created["id"]
    response = client.delete(f"/locations/{location_id}")
    assert response.status_code == 204


def test_get_after_delete(client):
    """Test retrieving a deleted location returns 404.

    Args:
        client: Shared test HTTP client fixture.
    """
    created = client.post("/locations/", json={"name": "GoneLocation"}).json()
    location_id = created["id"]
    client.delete(f"/locations/{location_id}")
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"
