"""FastAPI router for the Device resource.

This module registers all CRUD endpoints for devices under the /devices
prefix and delegates business logic to the device_service module.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate
from src.services import device_service

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=List[DeviceOut], status_code=status.HTTP_200_OK)
def list_devices(db: Session = Depends(get_db)):
    """Return a list of all devices.

    Args:
        db: Database session injected by FastAPI dependency.

    Returns:
        A list of DeviceOut serialised device records.
    """
    return device_service.get_all(db)


@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(data: DeviceCreate, db: Session = Depends(get_db)):
    """Create a new device record.

    Args:
        data: Validated device creation payload.
        db: Database session injected by FastAPI dependency.

    Returns:
        The newly created device as a DeviceOut instance.
    """
    return device_service.create(db, data)


@router.get("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def get_device(device_id: int, db: Session = Depends(get_db)):
    """Retrieve a single device by id.

    Args:
        device_id: Primary key of the device to retrieve.
        db: Database session injected by FastAPI dependency.

    Returns:
        The matching device as a DeviceOut instance.
    """
    return device_service.get_by_id(db, device_id)


@router.put("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def update_device(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)):
    """Update an existing device record.

    Args:
        device_id: Primary key of the device to update.
        data: Validated device update payload.
        db: Database session injected by FastAPI dependency.

    Returns:
        The updated device as a DeviceOut instance.
    """
    return device_service.update(db, device_id, data)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """Delete a device record.

    Args:
        device_id: Primary key of the device to delete.
        db: Database session injected by FastAPI dependency.
    """
    device_service.delete(db, device_id)
