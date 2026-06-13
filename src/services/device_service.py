"""Service layer for the Device resource.

This module implements business logic for CRUD operations on Device records,
including validation of foreign-key references and duplicate detection.

Typical usage::

    from src.services.device_service import get_all, get_by_id, create, update, delete
"""

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.device_type import DeviceType
from src.models.location import Location
from src.schemas.device import DeviceCreate, DeviceUpdate


def get_all(db: Session) -> List[Device]:
    """Return all Device records.

    Args:
        db: Active database session.

    Returns:
        List of Device ORM instances.
    """
    return db.query(Device).all()


def get_by_id(db: Session, device_id: int) -> Device:
    """Return a single Device by primary key.

    Args:
        db: Active database session.
        device_id: Primary key of the device to retrieve.

    Returns:
        The matching Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def create(db: Session, payload: DeviceCreate) -> Device:
    """Create and persist a new Device record.

    Args:
        db: Active database session.
        payload: Validated creation payload.

    Returns:
        The newly created Device ORM instance.

    Raises:
        HTTPException: 409 if a device with the same serial_number already exists.
        HTTPException: 404 if the referenced device_type_id does not exist.
        HTTPException: 404 if the referenced location_id does not exist.
    """
    existing = db.query(Device).filter(Device.serial_number == payload.serial_number).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Device with this serial_number already exists")

    device_type = db.query(DeviceType).filter(DeviceType.id == payload.device_type_id).first()
    if device_type is None:
        raise HTTPException(status_code=404, detail="DeviceType not found")

    if payload.location_id is not None:
        location = db.query(Location).filter(Location.id == payload.location_id).first()
        if location is None:
            raise HTTPException(status_code=404, detail="Location not found")

    device = Device(**payload.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update(db: Session, device_id: int, payload: DeviceUpdate) -> Device:
    """Apply a partial update to an existing Device record.

    Args:
        db: Active database session.
        device_id: Primary key of the device to update.
        payload: Validated update payload (all fields optional).

    Returns:
        The updated Device ORM instance.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
        HTTPException: 404 if the referenced device_type_id does not exist.
        HTTPException: 404 if the referenced location_id does not exist.
    """
    device = get_by_id(db, device_id)

    updates = payload.model_dump(exclude_unset=True)

    if "device_type_id" in updates:
        device_type = db.query(DeviceType).filter(DeviceType.id == updates["device_type_id"]).first()
        if device_type is None:
            raise HTTPException(status_code=404, detail="DeviceType not found")

    if "location_id" in updates and updates["location_id"] is not None:
        location = db.query(Location).filter(Location.id == updates["location_id"]).first()
        if location is None:
            raise HTTPException(status_code=404, detail="Location not found")

    for field, value in updates.items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)
    return device


def delete(db: Session, device_id: int) -> None:
    """Delete a Device record by primary key.

    Args:
        db: Active database session.
        device_id: Primary key of the device to delete.

    Raises:
        HTTPException: 404 if no device with the given ID exists.
    """
    device = get_by_id(db, device_id)
    db.delete(device)
    db.commit()
