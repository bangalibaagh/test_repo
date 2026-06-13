"""Business logic for the device_types resource."""

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate


def get_all(db: Session) -> List[DeviceType]:
    """Return all device types.

    Args:
        db: SQLAlchemy database session.

    Returns:
        List of DeviceType ORM instances.
    """
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int) -> DeviceType:
    """Return a single device type by primary key.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to retrieve.

    Returns:
        The matching DeviceType ORM instance.

    Raises:
        HTTPException: 404 if no device type with the given id exists.
    """
    instance = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="Device type not found")
    return instance


def create(db: Session, payload: DeviceTypeCreate) -> DeviceType:
    """Create and persist a new device type.

    Args:
        db: SQLAlchemy database session.
        payload: Validated creation payload.

    Returns:
        The newly created DeviceType ORM instance.

    Raises:
        HTTPException: 409 if a device type with the same name already exists.
    """
    existing = db.query(DeviceType).filter(DeviceType.name == payload.name).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Device type name already exists")
    instance = DeviceType(**payload.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update(db: Session, device_type_id: int, payload: DeviceTypeUpdate) -> DeviceType:
    """Update an existing device type.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to update.
        payload: Validated update payload.

    Returns:
        The updated DeviceType ORM instance.

    Raises:
        HTTPException: 404 if no device type with the given id exists.
    """
    instance = get_by_id(db, device_type_id)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instance, field, value)
    db.commit()
    db.refresh(instance)
    return instance


def delete(db: Session, device_type_id: int) -> None:
    """Delete a device type by primary key.

    Args:
        db: SQLAlchemy database session.
        device_type_id: Primary key of the device type to delete.

    Raises:
        HTTPException: 404 if no device type with the given id exists.
    """
    instance = get_by_id(db, device_type_id)
    db.delete(instance)
    db.commit()
