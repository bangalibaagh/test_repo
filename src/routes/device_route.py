"""API routes for the Device resource."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate
from src.services import device_service

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)) -> DeviceOut:
    """Create a new device.

    Args:
        payload: Validated request body containing device fields.
        db: Database session injected via dependency.

    Returns:
        DeviceOut: The newly created device.
    """
    return device_service.create_device(db, payload)


@router.get("/", response_model=List[DeviceOut], status_code=status.HTTP_200_OK)
def list_devices(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[DeviceOut]:
    """List all devices with optional pagination.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        db: Database session injected via dependency.

    Returns:
        List[DeviceOut]: A list of devices.
    """
    return device_service.list_devices(db, skip=skip, limit=limit)


@router.get("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def get_device(device_id: int, db: Session = Depends(get_db)) -> DeviceOut:
    """Retrieve a single device by ID.

    Args:
        device_id: Primary key of the device.
        db: Database session injected via dependency.

    Returns:
        DeviceOut: The matching device.
    """
    return device_service.get_device(db, device_id)


@router.put("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def update_device(
    device_id: int, payload: DeviceUpdate, db: Session = Depends(get_db)
) -> DeviceOut:
    """Update an existing device.

    Args:
        device_id: Primary key of the device to update.
        payload: Partial update data.
        db: Database session injected via dependency.

    Returns:
        DeviceOut: The updated device.
    """
    return device_service.update_device(db, device_id, payload)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a device by ID.

    Args:
        device_id: Primary key of the device to delete.
        db: Database session injected via dependency.

    Returns:
        None
    """
    device_service.delete_device(db, device_id)
