"""Tests for the health check endpoint."""


def test_health_returns_200(client):
    """Test that GET /health returns HTTP 200 and the expected JSON body.

    Args:
        client: The pytest fixture providing a configured TestClient.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
