"""Tests for the locations API endpoints."""

import pytest


CREATE_PAYLOAD = {
    "name": "Warehouse A",
    "address": "123 Main St",
    "latitude": 51.5,
    "longitude": -0.1,
}


def test_create_location_returns_201(client):
    """POST / should create a location and return 201 with the body."""
    response = client.post("/locations/", json=CREATE_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == CREATE_PAYLOAD["name"]
    assert body["address"] == CREATE_PAYLOAD["address"]
    assert body["latitude"] == CREATE_PAYLOAD["latitude"]
    assert body["longitude"] == CREATE_PAYLOAD["longitude"]
    assert "id" in body
    assert "created_at" in body


def test_get_all_locations_returns_200(client):
    """GET / should return 200 and a list."""
    client.post("/locations/", json=CREATE_PAYLOAD)
    response = client.get("/locations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_location_by_id_returns_200(client):
    """GET /{id} should return 200 and the correct record."""
    created = client.post("/locations/", json=CREATE_PAYLOAD).json()
    response = client.get(f"/locations/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_non_existent_location_returns_404(client):
    """GET /{id} for a missing record should return 404."""
    response = client.get("/locations/99999")
    assert response.status_code == 404


def test_update_location_returns_200(client):
    """PUT /{id} should update the record and return 200 with changed field."""
    created = client.post("/locations/", json=CREATE_PAYLOAD).json()
    response = client.put(
        f"/locations/{created['id']}", json={"address": "456 New Ave"}
    )
    assert response.status_code == 200
    assert response.json()["address"] == "456 New Ave"


def test_delete_location_returns_204(client):
    """DELETE /{id} should remove the record and return 204."""
    created = client.post("/locations/", json=CREATE_PAYLOAD).json()
    response = client.delete(f"/locations/{created['id']}")
    assert response.status_code == 204


def test_delete_non_existent_location_returns_404(client):
    """DELETE /{id} for a missing record should return 404."""
    response = client.delete("/locations/99999")
    assert response.status_code == 404


def test_duplicate_name_returns_409(client):
    """POST / with a duplicate name should return 409."""
    client.post("/locations/", json=CREATE_PAYLOAD)
    response = client.post("/locations/", json=CREATE_PAYLOAD)
    assert response.status_code == 409
