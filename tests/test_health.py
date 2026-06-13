"""Tests for the health check endpoint."""

from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    """GET /health should return HTTP 200 and a JSON body of {'status': 'ok'}.

    Args:
        client: The shared function-scoped TestClient fixture.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
