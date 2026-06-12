"""Tests for the health check endpoint."""


def test_health_returns_200(client):
    """Test that the health endpoint returns HTTP 200 and correct body.

    Args:
        client: The pytest fixture providing a configured test client.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
