"""Service functions for the device_types resource.

Provides CRUD operations with JSON-structured logging and HTTP error
handling for device type records.
"""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate

logger = logging.getLogger(__name__)


def get_device_types(db: Session, skip: int = 0, limit: int = 100) -> list[DeviceType]:
    """Retrieve a paginated list of device types.

    Args:
        db: The active database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of DeviceType ORM instances.
    """
    logger.info({"action": "get_device_types", "skip": skip, "limit": limit})
    return db.query(DeviceType).offset(skip).limit(limit).all()


def get_device_type(db: Session, device_type_id: int) -> DeviceType:
    """Retrieve a single device type by its ID.

    Args:
        db: The active database session.
        device_type_id: The primary key of the device type.

    Returns:
        The matching DeviceType ORM instance.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info({"action": "get_device_type", "device_type_id": device_type_id})
    instance = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="Device type not found")
    return instance


def create_device_type(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new device type record.

    Args:
        db: The active database session.
        data: Validated creation payload.

    Returns:
        The newly created DeviceType ORM instance.
    """
    logger.info({"action": "create_device_type", "name": data.name})
    instance = DeviceType(name=data.name, description=data.description)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_device_type(
    db: Session, device_type_id: int, data: DeviceTypeUpdate
) -> DeviceType:
    """Update an existing device type record.

    Args:
        db: The active database session.
        device_type_id: The primary key of the device type to update.
        data: Validated update payload.

    Returns:
        The updated DeviceType ORM instance.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info({"action": "update_device_type", "device_type_id": device_type_id})
    instance = get_device_type(db, device_type_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instance, field, value)
    db.commit()
    db.refresh(instance)
    return instance


def delete_device_type(db: Session, device_type_id: int) -> None:
    """Delete a device type record.

    Args:
        db: The active database session.
        device_type_id: The primary key of the device type to delete.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.info({"action": "delete_device_type", "device_type_id": device_type_id})
    instance = get_device_type(db, device_type_id)
    db.delete(instance)
    db.commit()
