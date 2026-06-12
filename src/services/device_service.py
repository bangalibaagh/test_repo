"""Service layer for Device CRUD operations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.device_type import DeviceType
from src.models.location import Location
from src.schemas.device import DeviceCreate, DeviceUpdate


def get_all(db: Session) -> List[Device]:
    """Retrieve all devices from the database.

    Args:
        db: SQLAlchemy database session.

    Returns:
        List of Device model instances.
    """
    return db.query(Device).all()


def get_by_id(db: Session, device_id: int) -> Optional[Device]:
    """Retrieve a single device by its primary key.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to retrieve.

    Returns:
        Device instance if found, otherwise None.
    """
    return db.query(Device).filter(Device.id == device_id).first()


def _validate_foreign_keys(db: Session, device_type_id: Optional[int], location_id: Optional[int]) -> None:
    """Validate that referenced foreign keys exist.

    Args:
        db: SQLAlchemy database session.
        device_type_id: ID of the device type to validate, or None to skip.
        location_id: ID of the location to validate, or None to skip.

    Raises:
        ValueError: If device_type_id does not reference an existing DeviceType.
        ValueError: If location_id does not reference an existing Location.
    """
    if device_type_id is not None:
        if not db.query(DeviceType).filter(DeviceType.id == device_type_id).first():
            raise ValueError("device_type not found")
    if location_id is not None:
        if not db.query(Location).filter(Location.id == location_id).first():
            raise ValueError("location not found")


def create(db: Session, data: DeviceCreate) -> Device:
    """Create a new device record.

    Args:
        db: SQLAlchemy database session.
        data: Validated DeviceCreate schema instance.

    Returns:
        Newly created Device model instance.

    Raises:
        ValueError: If device_type_id or location_id references a non-existent record.
    """
    _validate_foreign_keys(db, data.device_type_id, data.location_id)
    device = Device(**data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update(db: Session, device_id: int, data: DeviceUpdate) -> Optional[Device]:
    """Update an existing device record.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to update.
        data: Validated DeviceUpdate schema instance with fields to update.

    Returns:
        Updated Device model instance, or None if not found.

    Raises:
        ValueError: If device_type_id or location_id references a non-existent record.
    """
    device = get_by_id(db, device_id)
    if device is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    _validate_foreign_keys(
        db,
        update_data.get("device_type_id"),
        update_data.get("location_id"),
    )
    for field, value in update_data.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete(db: Session, device_id: int) -> bool:
    """Delete a device record by its primary key.

    Args:
        db: SQLAlchemy database session.
        device_id: Primary key of the device to delete.

    Returns:
        True if the device was deleted, False if it was not found.
    """
    device = get_by_id(db, device_id)
    if device is None:
        return False
    db.delete(device)
    db.commit()
    return True
