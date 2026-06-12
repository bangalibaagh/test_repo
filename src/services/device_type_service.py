"""Business logic for device type operations."""

import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate

logger = logging.getLogger(__name__)


def get_all(db: Session) -> List[DeviceType]:
    """Return all device type rows from the database.

    Args:
        db: The database session.

    Returns:
        A list of all DeviceType records.
    """
    logger.info("Fetching all device types")
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int) -> DeviceType:
    """Return a single device type by its ID.

    Args:
        db: The database session.
        device_type_id: The ID of the device type to retrieve.

    Returns:
        The DeviceType record with the given ID.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info("Fetching device type with id=%s", device_type_id)
    row = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if row is None:
        logger.warning("Device type id=%s not found", device_type_id)
        raise HTTPException(status_code=404, detail="Device type not found")
    return row


def create(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new device type record.

    Args:
        db: The database session.
        data: The input data for the new device type.

    Returns:
        The newly created DeviceType record.

    Raises:
        HTTPException: 409 if a device type with the same name already exists.
    """
    logger.info("Creating device type with name=%s", data.name)
    existing = db.query(DeviceType).filter(DeviceType.name == data.name).first()
    if existing is not None:
        logger.warning("Duplicate device type name=%s", data.name)
        raise HTTPException(status_code=409, detail="Device type name already exists")
    row = DeviceType(name=data.name, description=data.description)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, device_type_id: int, data: DeviceTypeUpdate) -> DeviceType:
    """Update an existing device type record.

    Args:
        db: The database session.
        device_type_id: The ID of the device type to update.
        data: The partial update data.

    Returns:
        The updated DeviceType record.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info("Updating device type id=%s", device_type_id)
    row = get_by_id(db, device_type_id)
    if data.name is not None:
        row.name = data.name
    if data.description is not None:
        row.description = data.description
    db.commit()
    db.refresh(row)
    return row


def delete(db: Session, device_type_id: int) -> None:
    """Delete a device type record.

    Args:
        db: The database session.
        device_type_id: The ID of the device type to delete.

    Returns:
        None

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info("Deleting device type id=%s", device_type_id)
    row = get_by_id(db, device_type_id)
    db.delete(row)
    db.commit()
    return None
