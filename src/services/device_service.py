"""Business logic for the Device resource."""

import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.device_type import DeviceType
from src.models.location import Location
from src.schemas.device import DeviceCreate, DeviceUpdate

logger = logging.getLogger(__name__)


def create_device(db: Session, payload: DeviceCreate) -> Device:
    """Create a new device record in the database.

    Verifies that the referenced device_type_id exists. If location_id is
    provided, also verifies that it exists.

    Args:
        db: SQLAlchemy database session.
        payload: Validated data for the new device.

    Returns:
        Device: The newly created Device ORM instance.

    Raises:
        HTTPException: 404 if device_type_id does not exist.
        HTTPException: 404 if location_id is provided but does not exist.
    """
    device_type = db.query(DeviceType).filter(DeviceType.id == payload.device_type_id).first()
    if not device_type:
        logger.warning("DeviceType id=%s not found", payload.device_type_id)
        raise HTTPException(status_code=404, detail="DeviceType not found")

    if payload.location_id is not None:
        location = db.query(Location).filter(Location.id == payload.location_id).first()
        if not location:
            logger.warning("Location id=%s not found", payload.location_id)
            raise HTTPException(status_code=404, detail="Location not found")

    device = Device(
        serial_number=payload.serial_number,
        name=payload.name,
        device_type_id=payload.device_type_id,
        location_id=payload.location_id,
        status=payload.status,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    logger.info("Created device id=%s", device.id)
    return device


def get_device(db: Session, device_id: int) -> Device:
    """Retrieve a single device by its primary key.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to retrieve.

    Returns:
        Device: The matching Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        logger.warning("Device id=%s not found", device_id)
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def list_devices(db: Session, skip: int = 0, limit: int = 100) -> List[Device]:
    """Return a paginated list of devices.

    Args:
        db: SQLAlchemy database session.
        skip: Number of records to skip (offset).
        limit: Maximum number of records to return.

    Returns:
        List[Device]: A list of Device ORM instances.
    """
    return db.query(Device).offset(skip).limit(limit).all()


def update_device(db: Session, device_id: int, payload: DeviceUpdate) -> Device:
    """Update an existing device with the provided fields.

    Only fields explicitly set in the payload are updated.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to update.
        payload: Partial update data.

    Returns:
        Device: The updated Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    device = get_device(db, device_id)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    logger.info("Updated device id=%s", device_id)
    return device


def delete_device(db: Session, device_id: int) -> None:
    """Delete a device by its primary key.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to delete.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    device = get_device(db, device_id)
    db.delete(device)
    db.commit()
    logger.info("Deleted device id=%s", device_id)
