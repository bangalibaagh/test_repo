"""Service layer for DeviceType CRUD operations."""

import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate

logger = logging.getLogger(__name__)


def get_device_type(db: Session, device_type_id: int) -> Optional[DeviceType]:
    """Retrieve a single device type by its ID.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to retrieve.

    Returns:
        The DeviceType instance if found, otherwise None.
    """
    result = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    logger.info({"action": "get_device_type", "device_type_id": device_type_id, "found": result is not None})
    return result


def get_device_types(db: Session, skip: int = 0, limit: int = 100) -> List[DeviceType]:
    """Retrieve a list of device types with optional pagination.

    Args:
        db: SQLAlchemy database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of DeviceType instances.
    """
    results = db.query(DeviceType).offset(skip).limit(limit).all()
    logger.info({"action": "get_device_types", "skip": skip, "limit": limit, "count": len(results)})
    return results


def create_device_type(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new device type.

    Args:
        db: SQLAlchemy database session.
        data: Pydantic schema containing the fields for the new device type.

    Returns:
        The newly created DeviceType instance.
    """
    device_type = DeviceType(name=data.name, description=data.description)
    db.add(device_type)
    db.commit()
    db.refresh(device_type)
    logger.info({"action": "create_device_type", "device_type_id": device_type.id, "name": device_type.name})
    return device_type


def update_device_type(db: Session, device_type_id: int, data: DeviceTypeUpdate) -> Optional[DeviceType]:
    """Update an existing device type.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to update.
        data: Pydantic schema containing the fields to update.

    Returns:
        The updated DeviceType instance if found, otherwise None.
    """
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if device_type is None:
        logger.info({"action": "update_device_type", "device_type_id": device_type_id, "found": False})
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device_type, field, value)
    db.commit()
    db.refresh(device_type)
    logger.info({"action": "update_device_type", "device_type_id": device_type_id, "found": True})
    return device_type


def delete_device_type(db: Session, device_type_id: int) -> bool:
    """Delete a device type by its ID.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to delete.

    Returns:
        True if the device type was deleted, False if not found.
    """
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if device_type is None:
        logger.info({"action": "delete_device_type", "device_type_id": device_type_id, "found": False})
        return False
    db.delete(device_type)
    db.commit()
    logger.info({"action": "delete_device_type", "device_type_id": device_type_id, "found": True})
    return True
