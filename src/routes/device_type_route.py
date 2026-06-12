"""FastAPI router for device type endpoints."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services import device_type_service

router = APIRouter(prefix="/device-types", tags=["device_types"])


@router.post("/", response_model=DeviceTypeOut, status_code=status.HTTP_201_CREATED)
def create_device_type(
    data: DeviceTypeCreate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Create a new device type.

    Args:
        data: Request body containing device type fields.
        db: Database session injected via dependency.

    Returns:
        DeviceTypeOut: The created device type.
    """
    return device_type_service.create_device_type(db, data)


@router.get("/", response_model=List[DeviceTypeOut], status_code=status.HTTP_200_OK)
def list_device_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[DeviceTypeOut]:
    """List all device types with optional pagination.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        db: Database session injected via dependency.

    Returns:
        list[DeviceTypeOut]: A list of device types.
    """
    return device_type_service.list_device_types(db, skip=skip, limit=limit)


@router.get("/{device_type_id}", response_model=DeviceTypeOut, status_code=status.HTTP_200_OK)
def get_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Retrieve a device type by ID.

    Args:
        device_type_id: Primary key of the device type.
        db: Database session injected via dependency.

    Returns:
        DeviceTypeOut: The requested device type.

    Raises:
        HTTPException: 404 if the device type does not exist.
    """
    return device_type_service.get_device_type(db, device_type_id)


@router.put("/{device_type_id}", response_model=DeviceTypeOut, status_code=status.HTTP_200_OK)
def update_device_type(
    device_type_id: int, data: DeviceTypeUpdate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Update an existing device type.

    Args:
        device_type_id: Primary key of the device type to update.
        data: Request body with fields to update.
        db: Database session injected via dependency.

    Returns:
        DeviceTypeOut: The updated device type.

    Raises:
        HTTPException: 404 if the device type does not exist.
    """
    return device_type_service.update_device_type(db, device_type_id, data)


@router.delete("/{device_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> None:
    """Delete a device type by ID.

    Args:
        device_type_id: Primary key of the device type to delete.
        db: Database session injected via dependency.

    Raises:
        HTTPException: 404 if the device type does not exist.
    """
    device_type_service.delete_device_type(db, device_type_id)
