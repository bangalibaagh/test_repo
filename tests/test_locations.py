"""Tests for the locations API endpoints.

This module covers CRUD operations for the /locations resource using
the shared ``client`` fixture from conftest.py.
"""


def test_list_locations_empty_returns_200(client):
    """GET /locations/ returns 200 with an empty list when no records exist."""
    response = client.get("/locations/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_location_returns_201(client):
    """POST /locations/ returns 201 with the created location data."""
    payload = {
        "name": "Warehouse A",
        "address": "123 Main St",
        "latitude": 51.5074,
        "longitude": -0.1278,
    }
    response = client.post("/locations/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Warehouse A"
    assert body["address"] == "123 Main St"
    assert body["latitude"] == 51.5074
    assert body["longitude"] == -0.1278
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_get_location_by_id_returns_200(client):
    """GET /locations/{id} returns 200 with the correct location."""
    create_resp = client.post("/locations/", json={"name": "Site B", "address": "456 Oak Ave"})
    location_id = create_resp.json()["id"]

    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == location_id
    assert body["name"] == "Site B"


def test_get_location_not_found_returns_404(client):
    """GET /locations/{id} returns 404 when the location does not exist."""
    response = client.get("/locations/99999")
    assert response.status_code == 404


def test_update_location_returns_200(client):
    """PUT /locations/{id} returns 200 with updated fields."""
    create_resp = client.post("/locations/", json={"name": "Depot C"})
    location_id = create_resp.json()["id"]

    update_payload = {"name": "Depot C Updated", "address": "789 Pine Rd"}
    response = client.put(f"/locations/{location_id}", json=update_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Depot C Updated"
    assert body["address"] == "789 Pine Rd"


def test_update_location_not_found_returns_404(client):
    """PUT /locations/{id} returns 404 when the location does not exist."""
    response = client.put("/locations/99999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_location_returns_204(client):
    """DELETE /locations/{id} returns 204 when the location is deleted."""
    create_resp = client.post("/locations/", json={"name": "Temp Location"})
    location_id = create_resp.json()["id"]

    response = client.delete(f"/locations/{location_id}")
    assert response.status_code == 204

    get_resp = client.get(f"/locations/{location_id}")
    assert get_resp.status_code == 404


def test_delete_location_not_found_returns_404(client):
    """DELETE /locations/{id} returns 404 when the location does not exist."""
    response = client.delete("/locations/99999")
    assert response.status_code == 404
