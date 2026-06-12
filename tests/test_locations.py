"""Tests for the locations API endpoints."""


def test_create_location_returns_201_with_fields(client):
    """Test that creating a location returns 201 and the correct fields.

    Args:
        client: The shared test client fixture.
    """
    payload = {
        "name": "Warehouse A",
        "address": "123 Main St",
        "latitude": 51.5,
        "longitude": -0.1,
    }
    response = client.post("/locations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Warehouse A"
    assert data["address"] == "123 Main St"
    assert data["latitude"] == 51.5
    assert data["longitude"] == -0.1
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_locations_returns_200(client):
    """Test that listing locations returns 200 and a list.

    Args:
        client: The shared test client fixture.
    """
    client.post("/locations/", json={"name": "Site B"})
    response = client.get("/locations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_location_by_id_returns_200(client):
    """Test that retrieving a location by id returns 200 and correct data.

    Args:
        client: The shared test client fixture.
    """
    created = client.post("/locations/", json={"name": "Site C"}).json()
    location_id = created["id"]
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 200
    assert response.json()["id"] == location_id
    assert response.json()["name"] == "Site C"


def test_update_location_returns_200_with_changed_field(client):
    """Test that updating a location returns 200 and reflects the change.

    Args:
        client: The shared test client fixture.
    """
    created = client.post("/locations/", json={"name": "Site D"}).json()
    location_id = created["id"]
    response = client.put(f"/locations/{location_id}", json={"name": "Site D Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "Site D Updated"


def test_delete_location_returns_204(client):
    """Test that deleting a location returns 204.

    Args:
        client: The shared test client fixture.
    """
    created = client.post("/locations/", json={"name": "Site E"}).json()
    location_id = created["id"]
    response = client.delete(f"/locations/{location_id}")
    assert response.status_code == 204


def test_get_deleted_location_returns_404(client):
    """Test that retrieving a deleted location returns 404.

    Args:
        client: The shared test client fixture.
    """
    created = client.post("/locations/", json={"name": "Site F"}).json()
    location_id = created["id"]
    client.delete(f"/locations/{location_id}")
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 404


def test_duplicate_name_returns_409(client):
    """Test that creating a location with a duplicate name returns 409.

    Args:
        client: The shared test client fixture.
    """
    client.post("/locations/", json={"name": "Unique Site"})
    response = client.post("/locations/", json={"name": "Unique Site"})
    assert response.status_code == 409
