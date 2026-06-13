"""Business logic for DeviceType operations.

This module provides service functions for CRUD operations on DeviceType
records, including validation and error handling.
"""

import json
import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate

logger = logging.getLogger(__name__)


def get_all(db: Session) -> list[DeviceType]:
    """Retrieve all DeviceType records.

    Args:
        db: The database session.

    Returns:
        A list of all DeviceType ORM instances.
    """
    logger.info(json.dumps({"action": "get_all_device_types"}))
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int) -> DeviceType:
    """Retrieve a DeviceType by its primary key.

    Args:
        db: The database session.
        device_type_id: The primary key of the device type to retrieve.

    Returns:
        The DeviceType ORM instance with the given id.

    Raises:
        HTTPException: 404 if no DeviceType with the given id exists.
    """
    logger.info(json.dumps({"action": "get_device_type_by_id", "id": device_type_id}))
    instance = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="DeviceType not found")
    return instance


def create(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new DeviceType record.

    Args:
        db: The database session.
        data: The validated creation payload.

    Returns:
        The newly created DeviceType ORM instance.

    Raises:
        HTTPException: 400 if a DeviceType with the same name already exists.
    """
    logger.info(json.dumps({"action": "create_device_type", "name": data.name}))
    existing = db.query(DeviceType).filter(DeviceType.name == data.name).first()
    if existing is not None:
        raise HTTPException(status_code=400, detail="DeviceType name already exists")
    instance = DeviceType(name=data.name, description=data.description)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update(db: Session, device_type_id: int, data: DeviceTypeUpdate) -> DeviceType:
    """Update an existing DeviceType record.

    Args:
        db: The database session.
        device_type_id: The primary key of the device type to update.
        data: The validated update payload.

    Returns:
        The updated DeviceType ORM instance.

    Raises:
        HTTPException: 404 if no DeviceType with the given id exists.
    """
    logger.info(json.dumps({"action": "update_device_type", "id": device_type_id}))
    instance = get_by_id(db, device_type_id)
    if data.name is not None:
        instance.name = data.name
    if data.description is not None:
        instance.description = data.description
    db.commit()
    db.refresh(instance)
    return instance


def delete(db: Session, device_type_id: int) -> None:
    """Delete a DeviceType record.

    Args:
        db: The database session.
        device_type_id: The primary key of the device type to delete.

    Raises:
        HTTPException: 404 if no DeviceType with the given id exists.
    """
    logger.info(json.dumps({"action": "delete_device_type", "id": device_type_id}))
    instance = get_by_id(db, device_type_id)
    db.delete(instance)
    db.commit()
