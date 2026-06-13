"""Business logic for the Location resource.

This module provides CRUD operations for Location records, raising
appropriate HTTP exceptions for error conditions.

Typical usage::

    from src.services.location_service import get_all, create
"""

from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate


def get_all(db: Session) -> List[Location]:
    """Return all Location records.

    Args:
        db: Active database session.

    Returns:
        List of all Location ORM instances.
    """
    return db.query(Location).all()


def get_by_id(location_id: int, db: Session) -> Location:
    """Return a single Location by primary key.

    Args:
        location_id: Primary key of the location to retrieve.
        db: Active database session.

    Returns:
        The matching Location ORM instance.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


def create(data: LocationCreate, db: Session) -> Location:
    """Create and persist a new Location.

    Args:
        data: Validated creation payload.
        db: Active database session.

    Returns:
        The newly created Location ORM instance.

    Raises:
        HTTPException: 409 if a location with the same name already exists.
    """
    location = Location(
        name=data.name,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    db.add(location)
    try:
        db.commit()
        db.refresh(location)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Location name already exists")
    return location


def update(location_id: int, data: LocationUpdate, db: Session) -> Location:
    """Update an existing Location.

    Args:
        location_id: Primary key of the location to update.
        data: Validated update payload (partial updates supported).
        db: Active database session.

    Returns:
        The updated Location ORM instance.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = get_by_id(location_id, db)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


def delete(location_id: int, db: Session) -> None:
    """Delete a Location by primary key.

    Args:
        location_id: Primary key of the location to delete.
        db: Active database session.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = get_by_id(location_id, db)
    db.delete(location)
    db.commit()
