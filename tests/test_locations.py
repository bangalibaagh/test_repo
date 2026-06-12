"""Tests for the locations CRUD endpoints."""

import pytest


BASE_URL = "/locations"


def test_create_location_returns_201(client):
    """POST /locations/ with valid data should return 201 and the created body."""
    payload = {"name": "HQ", "address": "123 Main St", "latitude": 1.23, "longitude": 4.56}
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "HQ"
    assert body["address"] == "123 Main St"
    assert body["latitude"] == 1.23
    assert body["longitude"] == 4.56
    assert "id" in body
    assert "created_at" in body


def test_create_duplicate_location_returns_400(client):
    """POST /locations/ with a duplicate name should return 400."""
    payload = {"name": "Unique Place"}
    client.post(BASE_URL + "/", json=payload)
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 400


def test_list_locations_returns_200(client):
    """GET /locations/ should return 200 and a list."""
    client.post(BASE_URL + "/", json={"name": "Location A"})
    client.post(BASE_URL + "/", json={"name": "Location B"})
    response = client.get(BASE_URL + "/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    names = [loc["name"] for loc in body]
    assert "Location A" in names
    assert "Location B" in names


def test_get_location_by_id_returns_200(client):
    """GET /locations/{id} for an existing location should return 200 and correct body."""
    created = client.post(BASE_URL + "/", json={"name": "Find Me"}).json()
    location_id = created["id"]
    response = client.get(f"{BASE_URL}/{location_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Find Me"


def test_get_missing_location_returns_404(client):
    """GET /locations/{id} for a non-existent location should return 404."""
    response = client.get(f"{BASE_URL}/999999")
    assert response.status_code == 404


def test_update_location_returns_200(client):
    """PUT /locations/{id} should return 200 and updated fields."""
    created = client.post(BASE_URL + "/", json={"name": "Old Name", "address": "Old Addr"}).json()
    location_id = created["id"]
    response = client.put(f"{BASE_URL}/{location_id}", json={"name": "New Name", "address": "New Addr"})
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "New Name"
    assert body["address"] == "New Addr"
    assert body["id"] == location_id


def test_update_missing_location_returns_404(client):
    """PUT /locations/{id} for a non-existent location should return 404."""
    response = client.put(f"{BASE_URL}/999999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_location_returns_204(client):
    """DELETE /locations/{id} for an existing location should return 204."""
    created = client.post(BASE_URL + "/", json={"name": "Delete Me"}).json()
    location_id = created["id"]
    response = client.delete(f"{BASE_URL}/{location_id}")
    assert response.status_code == 204
    # Confirm it is gone
    get_response = client.get(f"{BASE_URL}/{location_id}")
    assert get_response.status_code == 404


def test_delete_missing_location_returns_404(client):
    """DELETE /locations/{id} for a non-existent location should return 404."""
    response = client.delete(f"{BASE_URL}/999999")
    assert response.status_code == 404
