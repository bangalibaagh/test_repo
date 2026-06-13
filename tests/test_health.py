"""Tests for the GET /health endpoint."""

from tests.conftest import client  # noqa: F401


def test_health_returns_200(client):
    """Assert that GET /health returns HTTP 200 and body {'status': 'ok'}.

    Args:
        client: The TestClient fixture.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
