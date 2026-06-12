"""Business logic layer for DeviceType CRUD operations."""

from sqlalchemy.orm import Session

from src.models.device_type import DeviceType
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate


def get_all(db: Session) -> list[DeviceType]:
    """Retrieve all device types from the database.

    Args:
        db: The SQLAlchemy database session.

    Returns:
        A list of all DeviceType ORM instances.
    """
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int) -> DeviceType | None:
    """Retrieve a single device type by its primary key.

    Args:
        db: The SQLAlchemy database session.
        device_type_id: The integer primary key of the device type.

    Returns:
        The matching DeviceType instance, or None if not found.
    """
    return db.query(DeviceType).filter(DeviceType.id == device_type_id).first()


def create(db: Session, data: DeviceTypeCreate) -> DeviceType:
    """Create and persist a new device type.

    Args:
        db: The SQLAlchemy database session.
        data: A DeviceTypeCreate schema instance with the new record's data.

    Returns:
        The newly created and persisted DeviceType ORM instance.
    """
    device_type = DeviceType(
        name=data.name,
        description=data.description,
    )
    db.add(device_type)
    db.commit()
    db.refresh(device_type)
    return device_type


def update(
    db: Session, device_type_id: int, data: DeviceTypeUpdate
) -> DeviceType | None:
    """Update an existing device type with partial data.

    Args:
        db: The SQLAlchemy database session.
        device_type_id: The integer primary key of the device type to update.
        data: A DeviceTypeUpdate schema instance containing fields to update.

    Returns:
        The updated DeviceType ORM instance, or None if not found.
    """
    device_type = get_by_id(db, device_type_id)
    if device_type is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device_type, field, value)
    db.commit()
    db.refresh(device_type)
    return device_type


def delete(db: Session, device_type_id: int) -> bool:
    """Delete a device type by its primary key.

    Args:
        db: The SQLAlchemy database session.
        device_type_id: The integer primary key of the device type to delete.

    Returns:
        True if the record was found and deleted, False otherwise.
    """
    device_type = get_by_id(db, device_type_id)
    if device_type is None:
        return False
    db.delete(device_type)
    db.commit()
    return True
