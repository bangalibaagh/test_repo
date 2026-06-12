"""Tests for the devices vertical slice."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.config.database import Base, get_db

# Ensure all models are registered with Base.metadata before create_all
try:
    import src.device_types.model  # noqa: F401
except ModuleNotFoundError:
    pass
try:
    import src.devices.model  # noqa: F401
except ModuleNotFoundError:
    pass
try:
    import src.locations.model  # noqa: F401
except ModuleNotFoundError:
    pass

SQLITE_URL = "sqlite:///:memory:"

_engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test and drop them after.

    Yields:
        None
    """
    Base.metadata.create_all(bind=_engine)

    def override_get_db():
        db = _TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=_engine)


@pytest.fixture()
def client():
    """Return a TestClient for the FastAPI app.

    Returns:
        TestClient instance.
    """
    return TestClient(app)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def create_device_type(client: TestClient, name: str = "Sensor") -> dict:
    """Pre-create a device type via the API and return its JSON body.

    Args:
        client: TestClient instance.
        name: Name for the device type.

    Returns:
        Parsed JSON response body of the created device type.
    """
    response = client.post("/device-types/", json={"name": name, "description": "test type"})
    assert response.status_code == 201, response.text
    return response.json()


def create_location(client: TestClient, name: str = "Warehouse A") -> dict:
    """Pre-create a location via the API and return its JSON body.

    Args:
        client: TestClient instance.
        name: Name for the location.

    Returns:
        Parsed JSON response body of the created location.
    """
    response = client.post("/locations/", json={"name": name, "description": "test location"})
    assert response.status_code == 201, response.text
    return response.json()


def make_device_payload(
    device_type_id: int,
    serial_number: str = "SN-001",
    location_id: int = None,
) -> dict:
    """Build a device creation payload.

    Args:
        device_type_id: ID of an existing device type.
        serial_number: Serial number string for the device.
        location_id: Optional location ID.

    Returns:
        Dictionary suitable for posting to the devices endpoint.
    """
    payload = {
        "device_type_id": device_type_id,
        "serial_number": serial_number,
    }
    if location_id is not None:
        payload["location_id"] = location_id
    return payload


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_create_device_returns_201_and_body(client):
    """POST /devices/ should return 201 and the created device body."""
    dt = create_device_type(client)
    payload = make_device_payload(device_type_id=dt["id"])
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["serial_number"] == "SN-001"
    assert body["device_type_id"] == dt["id"]
    assert "id" in body


def test_create_device_duplicate_serial_returns_400(client):
    """POST /devices/ with a duplicate serial number should return 400."""
    dt = create_device_type(client)
    payload = make_device_payload(device_type_id=dt["id"], serial_number="SN-DUP")
    client.post("/devices/", json=payload)
    response = client.post("/devices/", json=payload)
    assert response.status_code == 400


def test_list_devices_returns_200_and_list(client):
    """GET /devices/ should return 200 and a list."""
    dt = create_device_type(client)
    client.post("/devices/", json=make_device_payload(dt["id"], "SN-A"))
    client.post("/devices/", json=make_device_payload(dt["id"], "SN-B"))
    response = client.get("/devices/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    serials = [d["serial_number"] for d in body]
    assert "SN-A" in serials
    assert "SN-B" in serials


def test_get_device_by_id_returns_200(client):
    """GET /devices/{id} should return 200 and the correct device."""
    dt = create_device_type(client)
    created = client.post("/devices/", json=make_device_payload(dt["id"])).json()
    response = client.get(f"/devices/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_device_returns_404(client):
    """GET /devices/{id} for a non-existent device should return 404."""
    response = client.get("/devices/99999")
    assert response.status_code == 404


def test_delete_device_returns_204(client):
    """DELETE /devices/{id} should return 204 for an existing device."""
    dt = create_device_type(client)
    created = client.post("/devices/", json=make_device_payload(dt["id"])).json()
    response = client.delete(f"/devices/{created['id']}")
    assert response.status_code == 204


def test_delete_missing_device_returns_404(client):
    """DELETE /devices/{id} for a non-existent device should return 404."""
    response = client.delete("/devices/99999")
    assert response.status_code == 404


def test_create_device_with_location_returns_201(client):
    """POST /devices/ with a location_id should return 201."""
    dt = create_device_type(client)
    loc = create_location(client)
    payload = make_device_payload(device_type_id=dt["id"], location_id=loc["id"])
    response = client.post("/devices/", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["location_id"] == loc["id"]
