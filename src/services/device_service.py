"""Business logic layer for the Device resource.

This module provides CRUD helper functions used by the device routes.
All database interactions are performed through the supplied SQLAlchemy
session. HTTPException is raised for client-facing error conditions.
"""

import logging
import json
from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.device_type import DeviceType
from src.models.location import Location
from src.schemas.device import DeviceCreate, DeviceUpdate


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
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


def get_all(db: Session) -> List[Device]:
    """Retrieve all device records.

    Args:
        db: Active SQLAlchemy database session.

    Returns:
        A list of Device ORM instances.
    """
    logger.info("Fetching all devices")
    return db.query(Device).all()


def get_by_id(db: Session, device_id: int) -> Device:
    """Retrieve a single device by primary key.

    Args:
        db: Active SQLAlchemy database session.
        device_id: Primary key of the device to retrieve.

    Returns:
        The matching Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given id exists.
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        logger.warning("Device not found", extra={"device_id": device_id})
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def create(db: Session, data: DeviceCreate) -> Device:
    """Create a new device record.

    Args:
        db: Active SQLAlchemy database session.
        data: Validated creation payload.

    Returns:
        The newly created Device ORM instance.

    Raises:
        HTTPException: 400 if the serial_number is already in use.
        HTTPException: 404 if device_type_id is provided but not found.
        HTTPException: 404 if location_id is provided but not found.
    """
    existing = db.query(Device).filter(Device.serial_number == data.serial_number).first()
    if existing:
        logger.warning("Duplicate serial_number", extra={"serial_number": data.serial_number})
        raise HTTPException(status_code=400, detail="serial_number already in use")

    if data.device_type_id is not None:
        dt = db.query(DeviceType).filter(DeviceType.id == data.device_type_id).first()
        if not dt:
            raise HTTPException(status_code=404, detail="DeviceType not found")

    if data.location_id is not None:
        loc = db.query(Location).filter(Location.id == data.location_id).first()
        if not loc:
            raise HTTPException(status_code=404, detail="Location not found")

    device = Device(
        serial_number=data.serial_number,
        name=data.name,
        status=data.status if data.status else "active",
        device_type_id=data.device_type_id,
        location_id=data.location_id,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    logger.info("Created device", extra={"device_id": device.id})
    return device


def update(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    """Update an existing device record.

    Args:
        db: Active SQLAlchemy database session.
        device_id: Primary key of the device to update.
        data: Validated update payload.

    Returns:
        The updated Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given id exists.
        HTTPException: 404 if device_type_id is provided but not found.
        HTTPException: 404 if location_id is provided but not found.
    """
    device = get_by_id(db, device_id)

    update_data = data.model_dump(exclude_unset=True)

    if "device_type_id" in update_data and update_data["device_type_id"] is not None:
        dt = db.query(DeviceType).filter(DeviceType.id == update_data["device_type_id"]).first()
        if not dt:
            raise HTTPException(status_code=404, detail="DeviceType not found")

    if "location_id" in update_data and update_data["location_id"] is not None:
        loc = db.query(Location).filter(Location.id == update_data["location_id"]).first()
        if not loc:
            raise HTTPException(status_code=404, detail="Location not found")

    for field, value in update_data.items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)
    logger.info("Updated device", extra={"device_id": device.id})
    return device


def delete(db: Session, device_id: int) -> None:
    """Delete a device record.

    Args:
        db: Active SQLAlchemy database session.
        device_id: Primary key of the device to delete.

    Raises:
        HTTPException: 404 if no device with the given id exists.
    """
    device = get_by_id(db, device_id)
    db.delete(device)
    db.commit()
    logger.info("Deleted device", extra={"device_id": device_id})
