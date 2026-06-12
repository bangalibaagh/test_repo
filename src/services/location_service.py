"""Service layer for Location CRUD operations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate


def get_all(db: Session) -> List[Location]:
    """Retrieve all locations from the database.

    Args:
        db: Active SQLAlchemy database session.

    Returns:
        A list of all Location ORM objects.
    """
    return db.query(Location).all()


def get_by_id(db: Session, location_id: int) -> Optional[Location]:
    """Retrieve a single location by its primary key.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to retrieve.

    Returns:
        The matching Location ORM object, or None if not found.
    """
    return db.query(Location).filter(Location.id == location_id).first()


def create(db: Session, data: LocationCreate) -> Location:
    """Create a new location record.

    Args:
        db: Active SQLAlchemy database session.
        data: Validated data for the new location.

    Returns:
        The newly created Location ORM object.
    """
    location = Location(**data.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update(db: Session, location_id: int, data: LocationUpdate) -> Optional[Location]:
    """Update an existing location record.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to update.
        data: Fields to update; unset fields are left unchanged.

    Returns:
        The updated Location ORM object, or None if not found.
    """
    location = get_by_id(db, location_id)
    if location is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


def delete(db: Session, location_id: int) -> bool:
    """Delete a location record.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to delete.

    Returns:
        True if the record was deleted, False if it was not found.
    """
    location = get_by_id(db, location_id)
    if location is None:
        return False
    db.delete(location)
    db.commit()
    return True
