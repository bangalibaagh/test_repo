"""FastAPI router for the devices resource."""

import logging
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate
from src.services import device_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=List[DeviceOut], status_code=status.HTTP_200_OK)
def list_devices(db: Session = Depends(get_db)) -> List[DeviceOut]:
    """List all devices.

    Args:
        db: SQLAlchemy database session provided by dependency injection.

    Returns:
        A list of DeviceOut objects.
    """
    logger.info("GET /devices/")
    return device_service.get_all(db)


@router.get("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def get_device(device_id: int, db: Session = Depends(get_db)) -> DeviceOut:
    """Retrieve a device by ID.

    Args:
        device_id: Primary key of the device to retrieve.
        db: SQLAlchemy database session provided by dependency injection.

    Returns:
        The DeviceOut object for the requested device.
    """
    logger.info("GET /devices/%s", device_id)
    return device_service.get_by_id(db, device_id)


@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(data: DeviceCreate, db: Session = Depends(get_db)) -> DeviceOut:
    """Create a new device.

    Args:
        data: Validated device creation payload.
        db: SQLAlchemy database session provided by dependency injection.

    Returns:
        The newly created DeviceOut object.
    """
    logger.info("POST /devices/")
    return device_service.create(db, data)


@router.put("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
def update_device(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)) -> DeviceOut:
    """Update an existing device.

    Args:
        device_id: Primary key of the device to update.
        data: Validated device update payload.
        db: SQLAlchemy database session provided by dependency injection.

    Returns:
        The updated DeviceOut object.
    """
    logger.info("PUT /devices/%s", device_id)
    return device_service.update(db, device_id, data)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a device by ID.

    Args:
        device_id: Primary key of the device to delete.
        db: SQLAlchemy database session provided by dependency injection.

    Returns:
        None
    """
    logger.info("DELETE /devices/%s", device_id)
    device_service.delete(db, device_id)
