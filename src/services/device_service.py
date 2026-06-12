"""Business logic for the devices resource."""

import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.device_type import DeviceType
from src.models.location import Location
from src.schemas.device import DeviceCreate, DeviceUpdate

logger = logging.getLogger(__name__)


def get_all(db: Session) -> List[Device]:
    """Retrieve all devices.

    Args:
        db: SQLAlchemy database session.

    Returns:
        A list of all Device records.
    """
    logger.info("Fetching all devices")
    return db.query(Device).all()


def get_by_id(db: Session, device_id: int) -> Device:
    """Retrieve a device by its primary key.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to retrieve.

    Returns:
        The Device record with the given ID.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    logger.info("Fetching device with id=%s", device_id)
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        logger.warning("Device id=%s not found", device_id)
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def create(db: Session, data: DeviceCreate) -> Device:
    """Create a new device.

    Args:
        db: SQLAlchemy database session.
        data: Validated device creation payload.

    Returns:
        The newly created Device record.

    Raises:
        HTTPException: 404 if device_type_id does not exist.
        HTTPException: 404 if location_id is provided but does not exist.
        HTTPException: 409 if serial_number is already in use.
    """
    logger.info("Creating device with serial_number=%s", data.serial_number)

    device_type = db.query(DeviceType).filter(DeviceType.id == data.device_type_id).first()
    if not device_type:
        logger.warning("DeviceType id=%s not found", data.device_type_id)
        raise HTTPException(status_code=404, detail="Device type not found")

    if data.location_id is not None:
        location = db.query(Location).filter(Location.id == data.location_id).first()
        if not location:
            logger.warning("Location id=%s not found", data.location_id)
            raise HTTPException(status_code=404, detail="Location not found")

    existing = db.query(Device).filter(Device.serial_number == data.serial_number).first()
    if existing:
        logger.warning("Duplicate serial_number=%s", data.serial_number)
        raise HTTPException(status_code=409, detail="Serial number already exists")

    device = Device(
        serial_number=data.serial_number,
        name=data.name,
        device_type_id=data.device_type_id,
        location_id=data.location_id,
        status=data.status,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    logger.info("Created device id=%s", device.id)
    return device


def update(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    """Update an existing device.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to update.
        data: Validated device update payload.

    Returns:
        The updated Device record.

    Raises:
        HTTPException: 404 if the device does not exist.
        HTTPException: 404 if device_type_id is updated but does not exist.
        HTTPException: 404 if location_id is updated but does not exist.
    """
    logger.info("Updating device id=%s", device_id)
    device = get_by_id(db, device_id)

    if data.device_type_id is not None:
        device_type = db.query(DeviceType).filter(DeviceType.id == data.device_type_id).first()
        if not device_type:
            logger.warning("DeviceType id=%s not found", data.device_type_id)
            raise HTTPException(status_code=404, detail="Device type not found")
        device.device_type_id = data.device_type_id

    if data.location_id is not None:
        location = db.query(Location).filter(Location.id == data.location_id).first()
        if not location:
            logger.warning("Location id=%s not found", data.location_id)
            raise HTTPException(status_code=404, detail="Location not found")
        device.location_id = data.location_id

    if data.serial_number is not None:
        device.serial_number = data.serial_number
    if data.name is not None:
        device.name = data.name
    if data.status is not None:
        device.status = data.status

    db.commit()
    db.refresh(device)
    logger.info("Updated device id=%s", device_id)
    return device


def delete(db: Session, device_id: int) -> None:
    """Delete a device by its primary key.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to delete.

    Raises:
        HTTPException: 404 if the device does not exist.
    """
    logger.info("Deleting device id=%s", device_id)
    device = get_by_id(db, device_id)
    db.delete(device)
    db.commit()
    logger.info("Deleted device id=%s", device_id)
