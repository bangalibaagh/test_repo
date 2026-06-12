"""Service functions for DeviceType CRUD operations."""

import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate

logger = logging.getLogger(__name__)


def get_all(db: Session) -> List[DeviceType]:
    """Retrieve all device types from the database.

    Args:
        db: SQLAlchemy database session.

    Returns:
        A list of all DeviceType records.
    """
    logger.info("Fetching all device types")
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int) -> DeviceType:
    """Retrieve a single device type by its ID.

    Args:
        db: SQLAlchemy database session.
        device_type_id: The primary key of the device type.

    Returns:
        The DeviceType record with the given ID.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info("Fetching device type id=%s", device_type_id)
    record = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if record is None:
        logger.warning("Device type id=%s not found", device_type_id)
        raise HTTPException(status_code=404, detail="Device type not found")
    return record


def create(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new device type.

    Args:
        db: SQLAlchemy database session.
        data: Validated input data for the new device type.

    Returns:
        The newly created DeviceType record.

    Raises:
        HTTPException: 409 if a device type with the same name already exists.
    """
    logger.info("Creating device type name=%s", data.name)
    existing = db.query(DeviceType).filter(DeviceType.name == data.name).first()
    if existing is not None:
        logger.warning("Duplicate device type name=%s", data.name)
        raise HTTPException(status_code=409, detail="Device type with this name already exists")
    record = DeviceType(name=data.name, description=data.description)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update(db: Session, device_type_id: int, data: DeviceTypeUpdate) -> DeviceType:
    """Update an existing device type.

    Args:
        db: SQLAlchemy database session.
        device_type_id: The primary key of the device type to update.
        data: Validated input data with fields to update.

    Returns:
        The updated DeviceType record.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info("Updating device type id=%s", device_type_id)
    record = get_by_id(db, device_type_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


def delete(db: Session, device_type_id: int) -> None:
    """Delete a device type by its ID.

    Args:
        db: SQLAlchemy database session.
        device_type_id: The primary key of the device type to delete.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info("Deleting device type id=%s", device_type_id)
    record = get_by_id(db, device_type_id)
    db.delete(record)
    db.commit()
