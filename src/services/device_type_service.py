"""Business logic layer for the DeviceType resource.

This module provides CRUD helper functions used by the device_type routes.
All database interactions are performed through the supplied SQLAlchemy
session. HTTPException is raised for client-facing error conditions.
"""

import logging
import json
from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_object["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_object)


def _get_logger(name: str) -> logging.Logger:
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


logger = _get_logger(__name__)


def get_all(db: Session) -> List[DeviceType]:
    """Retrieve all device type records.

    Args:
        db: Active SQLAlchemy database session.

    Returns:
        A list of DeviceType ORM instances.
    """
    logger.info("Fetching all device types")
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int) -> DeviceType:
    """Retrieve a single device type by primary key.

    Args:
        db: Active SQLAlchemy database session.
        device_type_id: Primary key of the device type to retrieve.

    Returns:
        The matching DeviceType ORM instance.

    Raises:
        HTTPException: 404 if no device type with the given id exists.
    """
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if not device_type:
        logger.warning("DeviceType not found with id %s", device_type_id)
        raise HTTPException(status_code=404, detail="DeviceType not found")
    return device_type


def create(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create a new device type record.

    Args:
        db: Active SQLAlchemy database session.
        data: Validated creation payload.

    Returns:
        The newly created DeviceType ORM instance.

    Raises:
        HTTPException: 400 if the name is already in use.
    """
    existing = db.query(DeviceType).filter(DeviceType.name == data.name).first()
    if existing:
        logger.warning("Duplicate device type name: %s", data.name)
        raise HTTPException(status_code=400, detail="Device type name already in use")

    device_type = DeviceType(
        name=data.name,
        description=getattr(data, "description", None),
    )
    db.add(device_type)
    db.commit()
    db.refresh(device_type)
    logger.info("Created device type with id %s", device_type.id)
    return device_type


def update(db: Session, device_type_id: int, data: DeviceTypeUpdate) -> DeviceType:
    """Update an existing device type record.

    Args:
        db: Active SQLAlchemy database session.
        device_type_id: Primary key of the device type to update.
        data: Validated update payload.

    Returns:
        The updated DeviceType ORM instance.

    Raises:
        HTTPException: 404 if no device type with the given id exists.
        HTTPException: 400 if the new name is already used by another device type.
    """
    device_type = get_by_id(db, device_type_id)

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data:
        conflict = (
            db.query(DeviceType)
            .filter(
                DeviceType.name == update_data["name"],
                DeviceType.id != device_type_id,
            )
            .first()
        )
        if conflict:
            logger.warning("Duplicate device type name on update: %s", update_data["name"])
            raise HTTPException(status_code=400, detail="Device type name already in use")

    for field, value in update_data.items():
        setattr(device_type, field, value)

    db.commit()
    db.refresh(device_type)
    logger.info("Updated device type with id %s", device_type_id)
    return device_type


def delete(db: Session, device_type_id: int) -> None:
    """Delete a device type record.

    Args:
        db: Active SQLAlchemy database session.
        device_type_id: Primary key of the device type to delete.

    Raises:
        HTTPException: 404 if no device type with the given id exists.
    """
    device_type = get_by_id(db, device_type_id)
    db.delete(device_type)
    db.commit()
    logger.info("Deleted device type with id %s", device_type_id)
