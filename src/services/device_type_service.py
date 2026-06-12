"""Business logic layer for device type CRUD operations."""

import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate

logger = logging.getLogger(__name__)


def create_device_type(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new device type record in the database.

    Args:
        db: SQLAlchemy database session.
        data: Validated data for the new device type.

    Returns:
        DeviceType: The newly created device type instance.
    """
    logger.debug("Creating device type with name=%s", data.name)
    device_type = DeviceType(name=data.name, description=data.description)
    db.add(device_type)
    db.commit()
    db.refresh(device_type)
    return device_type


def get_device_type(db: Session, device_type_id: int) -> DeviceType:
    """Retrieve a single device type by its ID.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to retrieve.

    Returns:
        DeviceType: The device type instance with the given ID.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.debug("Fetching device type id=%s", device_type_id)
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if device_type is None:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type


def list_device_types(db: Session, skip: int = 0, limit: int = 100) -> List[DeviceType]:
    """Return a paginated list of device types.

    Args:
        db: SQLAlchemy database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        list[DeviceType]: A list of device type instances.
    """
    logger.debug("Listing device types skip=%s limit=%s", skip, limit)
    return db.query(DeviceType).offset(skip).limit(limit).all()


def update_device_type(db: Session, device_type_id: int, data: DeviceTypeUpdate) -> DeviceType:
    """Update an existing device type record.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to update.
        data: Fields to update on the device type.

    Returns:
        DeviceType: The updated device type instance.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.debug("Updating device type id=%s", device_type_id)
    device_type = get_device_type(db, device_type_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device_type, field, value)
    db.commit()
    db.refresh(device_type)
    return device_type


def delete_device_type(db: Session, device_type_id: int) -> None:
    """Delete a device type record from the database.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to delete.

    Raises:
        HTTPException: 404 if no device type with the given ID exists.
    """
    logger.debug("Deleting device type id=%s", device_type_id)
    device_type = get_device_type(db, device_type_id)
    db.delete(device_type)
    db.commit()
