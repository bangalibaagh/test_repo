"""Tests for the health check endpoint."""

from starlette.testclient import TestClient

from src.main import app


def test_health_returns_200(client):
    """Test that GET /health returns HTTP 200 and the expected JSON body.

    Args:
        client: A ``TestClient`` fixture provided by conftest.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_missing_api_key_returns_401():
    """Test that GET /health without X-API-Key header returns HTTP 401."""
    with TestClient(app, headers={}) as c:
        response = c.get("/health")
    assert response.status_code == 401


def test_health_invalid_api_key_returns_401():
    """Test that GET /health with a wrong X-API-Key header returns HTTP 401."""
    with TestClient(app, headers={"X-API-Key": "wrong-key"}) as c:
        response = c.get("/health")
    assert response.status_code == 401
