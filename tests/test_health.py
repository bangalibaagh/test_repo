"""Tests for the health-check endpoint."""

from starlette.testclient import TestClient

from src.main import app


def test_health_returns_200() -> None:
    """GET /health should return HTTP 200 with body {'status': 'ok'}."""
    test_client = TestClient(app)
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
