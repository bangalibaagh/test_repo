"""Business logic for DeviceType operations.

This module provides service functions for CRUD operations on DeviceType
records, with JSON-compatible INFO-level logging.
"""

import logging

from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate

logger = logging.getLogger(__name__)


def get_all(db: Session) -> list[DeviceType]:
    """Retrieve all device types from the database.

    Args:
        db: Active SQLAlchemy database session.

    Returns:
        A list of all DeviceType records.
    """
    logger.info({"action": "get_all_device_types"})
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int) -> DeviceType | None:
    """Retrieve a single device type by its primary key.

    Args:
        db: Active SQLAlchemy database session.
        device_type_id: Primary key of the device type to retrieve.

    Returns:
        The DeviceType record if found, otherwise None.
    """
    logger.info({"action": "get_device_type_by_id", "device_type_id": device_type_id})
    return db.query(DeviceType).filter(DeviceType.id == device_type_id).first()


def create(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new device type record.

    Args:
        db: Active SQLAlchemy database session.
        data: Validated data for the new device type.

    Returns:
        The newly created DeviceType record.
    """
    logger.info({"action": "create_device_type", "name": data.name})
    device_type = DeviceType(**data.model_dump())
    db.add(device_type)
    db.commit()
    db.refresh(device_type)
    return device_type


def update(db: Session, device_type_id: int, data: DeviceTypeUpdate) -> DeviceType | None:
    """Update an existing device type record.

    Args:
        db: Active SQLAlchemy database session.
        device_type_id: Primary key of the device type to update.
        data: Validated partial data to apply to the record.

    Returns:
        The updated DeviceType record if found, otherwise None.
    """
    logger.info({"action": "update_device_type", "device_type_id": device_type_id})
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if device_type is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(device_type, field, value)
    db.commit()
    db.refresh(device_type)
    return device_type


def delete(db: Session, device_type_id: int) -> bool:
    """Delete a device type record by its primary key.

    Args:
        db: Active SQLAlchemy database session.
        device_type_id: Primary key of the device type to delete.

    Returns:
        True if the record was deleted, False if it was not found.
    """
    logger.info({"action": "delete_device_type", "device_type_id": device_type_id})
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if device_type is None:
        return False
    db.delete(device_type)
    db.commit()
    return True
