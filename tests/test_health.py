"""Tests for the GET /health endpoint."""


def test_health_returns_200(client):
    """Test that the health endpoint returns HTTP 200 and correct JSON body.

    Args:
        client: The pytest fixture providing a configured TestClient instance.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
