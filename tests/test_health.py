"""Tests for the GET /health endpoint."""

from tests.conftest import client  # noqa: F401


def test_health_returns_200(client):
    """Test that GET /health returns HTTP 200 and the expected JSON body.

    Args:
        client: The pytest fixture providing a configured test HTTP client.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
