"""Device routes module.

Defines the APIRouter and HTTP endpoints for the devices resource.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate
from src.services.device_service import (
    create_device,
    delete_device,
    get_device,
    get_devices,
    update_device,
)

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[DeviceOut], status_code=status.HTTP_200_OK)
def list_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[DeviceOut]:
    """Retrieve a paginated list of devices.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        db: Database session injected by dependency.

    Returns:
        A list of DeviceOut response models.
    """
    return get_devices(db, skip=skip, limit=limit)


@router.get("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def get_device_by_id(device_id: int, db: Session = Depends(get_db)) -> DeviceOut:
    """Retrieve a single device by ID.

    Args:
        device_id: Primary key of the device.
        db: Database session injected by dependency.

    Returns:
        The matching DeviceOut response model.
    """
    return get_device(db, device_id)


@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_new_device(data: DeviceCreate, db: Session = Depends(get_db)) -> DeviceOut:
    """Create a new device.

    Args:
        data: Validated device creation payload.
        db: Database session injected by dependency.

    Returns:
        The created DeviceOut response model.
    """
    return create_device(db, data)


@router.put("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def update_existing_device(
    device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)
) -> DeviceOut:
    """Update an existing device.

    Args:
        device_id: Primary key of the device to update.
        data: Validated device update payload.
        db: Database session injected by dependency.

    Returns:
        The updated DeviceOut response model.
    """
    return update_device(db, device_id, data)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_device(device_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a device.

    Args:
        device_id: Primary key of the device to delete.
        db: Database session injected by dependency.
    """
    delete_device(db, device_id)
