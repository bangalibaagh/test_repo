"""FastAPI router for Device endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate
from src.services import device_service

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=DeviceOut, status_code=201)
def create_device(data: DeviceCreate, db: Session = Depends(get_db)) -> DeviceOut:
    """Create a new device.

    Args:
        data: Validated DeviceCreate payload.
        db: Database session injected by FastAPI.

    Returns:
        The newly created device.

    Raises:
        HTTPException: 422 if a referenced foreign key does not exist.
        HTTPException: 400 if a database integrity constraint is violated.
    """
    try:
        return device_service.create(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error") from exc


@router.get("/", response_model=List[DeviceOut], status_code=200)
def list_devices(db: Session = Depends(get_db)) -> List[DeviceOut]:
    """List all devices.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        List of all device records.
    """
    return device_service.get_all(db)


@router.get("/{device_id}", response_model=DeviceOut, status_code=200)
def get_device(device_id: int, db: Session = Depends(get_db)) -> DeviceOut:
    """Retrieve a device by its ID.

    Args:
        device_id: Primary key of the device.
        db: Database session injected by FastAPI.

    Returns:
        The requested device.

    Raises:
        HTTPException: 404 if the device does not exist.
    """
    device = device_service.get_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=DeviceOut, status_code=200)
def update_device(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)) -> DeviceOut:
    """Update an existing device.

    Args:
        device_id: Primary key of the device to update.
        data: Validated DeviceUpdate payload.
        db: Database session injected by FastAPI.

    Returns:
        The updated device.

    Raises:
        HTTPException: 404 if the device does not exist.
        HTTPException: 422 if a referenced foreign key does not exist.
    """
    try:
        device = device_service.update(db, device_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a device by its ID.

    Args:
        device_id: Primary key of the device to delete.
        db: Database session injected by FastAPI.

    Raises:
        HTTPException: 404 if the device does not exist.
    """
    deleted = device_service.delete(db, device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device not found")
