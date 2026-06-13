"""FastAPI router for device_types endpoints.

This module defines the CRUD routes for DeviceType resources.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services import device_type_service

router = APIRouter(prefix="/device-types", tags=["device_types"])


@router.get("/", response_model=List[DeviceTypeOut], status_code=status.HTTP_200_OK)
def list_device_types(db: Session = Depends(get_db)) -> List[DeviceTypeOut]:
    """List all device types.

    Args:
        db: The database session provided by dependency injection.

    Returns:
        A list of all DeviceTypeOut instances.
    """
    return device_type_service.get_all(db)


@router.post("/", response_model=DeviceTypeOut, status_code=status.HTTP_201_CREATED)
def create_device_type(
    data: DeviceTypeCreate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Create a new device type.

    Args:
        data: The creation payload.
        db: The database session provided by dependency injection.

    Returns:
        The newly created DeviceTypeOut instance.
    """
    return device_type_service.create(db, data)


@router.get(
    "/{device_type_id}", response_model=DeviceTypeOut, status_code=status.HTTP_200_OK
)
def get_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Retrieve a device type by id.

    Args:
        device_type_id: The primary key of the device type.
        db: The database session provided by dependency injection.

    Returns:
        The DeviceTypeOut instance with the given id.
    """
    return device_type_service.get_by_id(db, device_type_id)


@router.put(
    "/{device_type_id}", response_model=DeviceTypeOut, status_code=status.HTTP_200_OK
)
def update_device_type(
    device_type_id: int, data: DeviceTypeUpdate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Update an existing device type.

    Args:
        device_type_id: The primary key of the device type to update.
        data: The update payload.
        db: The database session provided by dependency injection.

    Returns:
        The updated DeviceTypeOut instance.
    """
    return device_type_service.update(db, device_type_id, data)


@router.delete("/{device_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> None:
    """Delete a device type.

    Args:
        device_type_id: The primary key of the device type to delete.
        db: The database session provided by dependency injection.
    """
    device_type_service.delete(db, device_type_id)
