"""Tests for the device_types CRUD endpoints.

This module covers all happy-path and error-path scenarios for the
/device-types/ router using the shared ``client`` fixture.
"""


def test_list_device_types_empty(client):
    """GET /device-types/ returns 200 and an empty list when no records exist.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.get("/device-types/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_device_type(client):
    """POST /device-types/ returns 201 and the created resource fields.

    Args:
        client: The shared TestClient fixture.
    """
    payload = {"name": "Sensor", "description": "A sensor device"}
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["name"] == "Sensor"


def test_create_device_type_duplicate_name(client):
    """POST /device-types/ with a duplicate name returns 400.

    Args:
        client: The shared TestClient fixture.
    """
    payload = {"name": "Sensor", "description": "A sensor device"}
    client.post("/device-types/", json=payload)
    response = client.post("/device-types/", json=payload)
    assert response.status_code == 400


def test_get_device_type(client):
    """GET /device-types/{id} returns 200 and the correct resource.

    Args:
        client: The shared TestClient fixture.
    """
    create_response = client.post("/device-types/", json={"name": "Camera"})
    device_type_id = create_response.json()["id"]
    response = client.get(f"/device-types/{device_type_id}")
    assert response.status_code == 200
    assert response.json()["id"] == device_type_id


def test_get_device_type_not_found(client):
    """GET /device-types/9999 returns 404 when the resource does not exist.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.get("/device-types/9999")
    assert response.status_code == 404


def test_update_device_type(client):
    """PUT /device-types/{id} returns 200 and the updated resource fields.

    Args:
        client: The shared TestClient fixture.
    """
    create_response = client.post("/device-types/", json={"name": "OldName"})
    device_type_id = create_response.json()["id"]
    response = client.put(
        f"/device-types/{device_type_id}", json={"name": "NewName"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "NewName"


def test_update_device_type_not_found(client):
    """PUT /device-types/9999 returns 404 when the resource does not exist.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.put("/device-types/9999", json={"name": "DoesNotMatter"})
    assert response.status_code == 404


def test_update_device_type_duplicate_name(client):
    """PUT /device-types/{id} with a name already used by another record returns 400.

    The service checks for duplicate names when renaming a DeviceType and
    should raise 400 rather than allowing a DB constraint violation.

    Args:
        client: The shared TestClient fixture.
    """
    client.post("/device-types/", json={"name": "TypeAlpha"})
    second = client.post("/device-types/", json={"name": "TypeBeta"})
    second_id = second.json()["id"]
    response = client.put(f"/device-types/{second_id}", json={"name": "TypeAlpha"})
    assert response.status_code == 400


def test_delete_device_type(client):
    """DELETE /device-types/{id} returns 204 and the record is gone.

    Args:
        client: The shared TestClient fixture.
    """
    create_response = client.post("/device-types/", json={"name": "ToDelete"})
    device_type_id = create_response.json()["id"]
    delete_response = client.delete(f"/device-types/{device_type_id}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/device-types/{device_type_id}")
    assert get_response.status_code == 404


def test_delete_device_type_not_found(client):
    """DELETE /device-types/9999 returns 404 when the resource does not exist.

    Args:
        client: The shared TestClient fixture.
    """
    response = client.delete("/device-types/9999")
    assert response.status_code == 404
