"""FastAPI router for device type endpoints."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services import device_type_service

router = APIRouter(prefix="/device-types", tags=["device_types"])


@router.get("/", response_model=List[DeviceTypeOut], status_code=200)
def list_device_types(db: Session = Depends(get_db)) -> List[DeviceTypeOut]:
    """Return all device types.

    Args:
        db: The database session provided by dependency injection.

    Returns:
        A list of all DeviceTypeOut records.
    """
    return device_type_service.get_all(db)


@router.get("/{device_type_id}", response_model=DeviceTypeOut, status_code=200)
def get_device_type(device_type_id: int, db: Session = Depends(get_db)) -> DeviceTypeOut:
    """Return a single device type by ID.

    Args:
        device_type_id: The ID of the device type to retrieve.
        db: The database session provided by dependency injection.

    Returns:
        The DeviceTypeOut record for the given ID.
    """
    return device_type_service.get_by_id(db, device_type_id)


@router.post("/", response_model=DeviceTypeOut, status_code=201)
def create_device_type(data: DeviceTypeCreate, db: Session = Depends(get_db)) -> DeviceTypeOut:
    """Create a new device type.

    Args:
        data: The input data for the new device type.
        db: The database session provided by dependency injection.

    Returns:
        The newly created DeviceTypeOut record.
    """
    return device_type_service.create(db, data)


@router.put("/{device_type_id}", response_model=DeviceTypeOut, status_code=200)
def update_device_type(
    device_type_id: int, data: DeviceTypeUpdate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Update an existing device type.

    Args:
        device_type_id: The ID of the device type to update.
        data: The partial update data.
        db: The database session provided by dependency injection.

    Returns:
        The updated DeviceTypeOut record.
    """
    return device_type_service.update(db, device_type_id, data)


@router.delete("/{device_type_id}", status_code=204)
def delete_device_type(device_type_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a device type by ID.

    Args:
        device_type_id: The ID of the device type to delete.
        db: The database session provided by dependency injection.

    Returns:
        An empty response with HTTP 204 status.
    """
    device_type_service.delete(db, device_type_id)
