"""API routes for the Device resource.

This module defines the FastAPI router with CRUD endpoints for devices.

Typical usage::

    from src.routes.device_route import router as device_router
    app.include_router(device_router)
"""

from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate
from src.services import device_service

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=List[DeviceOut], status_code=200)
def list_devices(db: Session = Depends(get_db)) -> List[DeviceOut]:
    """Return all devices.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        List of DeviceOut instances.
    """
    return device_service.get_all(db)


@router.get("/{device_id}", response_model=DeviceOut, status_code=200)
def get_device(device_id: int, db: Session = Depends(get_db)) -> DeviceOut:
    """Return a single device by ID.

    Args:
        device_id: Primary key of the device.
        db: Database session injected by FastAPI.

    Returns:
        DeviceOut instance for the requested device.

    Raises:
        HTTPException: 404 if the device does not exist.
    """
    return device_service.get_by_id(db, device_id)


@router.post("/", response_model=DeviceOut, status_code=201)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)) -> DeviceOut:
    """Create a new device.

    Args:
        payload: Validated device creation data.
        db: Database session injected by FastAPI.

    Returns:
        DeviceOut instance for the newly created device.

    Raises:
        HTTPException: 409 if serial_number already exists.
        HTTPException: 404 if device_type_id or location_id is invalid.
    """
    return device_service.create(db, payload)


@router.put("/{device_id}", response_model=DeviceOut, status_code=200)
def update_device(
    device_id: int, payload: DeviceUpdate, db: Session = Depends(get_db)
) -> DeviceOut:
    """Update an existing device.

    Args:
        device_id: Primary key of the device to update.
        payload: Validated partial update data.
        db: Database session injected by FastAPI.

    Returns:
        DeviceOut instance with updated fields.

    Raises:
        HTTPException: 404 if the device, device_type_id, or location_id does not exist.
    """
    return device_service.update(db, device_id, payload)


@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: int, db: Session = Depends(get_db)) -> Response:
    """Delete a device by ID.

    Args:
        device_id: Primary key of the device to delete.
        db: Database session injected by FastAPI.

    Returns:
        Empty response with 204 status.

    Raises:
        HTTPException: 404 if the device does not exist.
    """
    device_service.delete(db, device_id)
    return Response(status_code=204)
