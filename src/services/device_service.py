"""Device service module.

Provides CRUD operations for the devices resource with JSON-structured
logging and HTTP error handling.
"""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.device_type import DeviceType
from src.schemas.device import DeviceCreate, DeviceUpdate

logger = logging.getLogger(__name__)


def get_devices(db: Session, skip: int = 0, limit: int = 100) -> list[Device]:
    """Retrieve a paginated list of devices.

    Args:
        db: Active database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of Device ORM instances.
    """
    logger.info({"action": "get_devices", "skip": skip, "limit": limit})
    return db.query(Device).offset(skip).limit(limit).all()


def get_device(db: Session, device_id: int) -> Device:
    """Retrieve a single device by its primary key.

    Args:
        db: Active database session.
        device_id: Primary key of the device to retrieve.

    Returns:
        The matching Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    logger.info({"action": "get_device", "device_id": device_id})
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def create_device(db: Session, data: DeviceCreate) -> Device:
    """Create a new device record.

    Args:
        db: Active database session.
        data: Validated device creation payload.

    Returns:
        The newly created Device ORM instance.

    Raises:
        HTTPException: 404 if the referenced device_type_id does not exist.
    """
    logger.info({"action": "create_device", "data": data.model_dump()})
    device_type = db.query(DeviceType).filter(DeviceType.id == data.device_type_id).first()
    if device_type is None:
        raise HTTPException(status_code=404, detail="DeviceType not found")
    device = Device(**data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    """Update an existing device record.

    Args:
        db: Active database session.
        device_id: Primary key of the device to update.
        data: Validated device update payload.

    Returns:
        The updated Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    logger.info({"action": "update_device", "device_id": device_id, "data": data.model_dump()})
    device = get_device(db, device_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int) -> None:
    """Delete a device record.

    Args:
        db: Active database session.
        device_id: Primary key of the device to delete.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    logger.info({"action": "delete_device", "device_id": device_id})
    device = get_device(db, device_id)
    db.delete(device)
    db.commit()
