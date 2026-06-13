"""Business logic layer for Location CRUD operations.

This module provides service functions that interact with the database
for creating, reading, updating, and deleting Location records.
"""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate

logger = logging.getLogger(__name__)


def get_all(db: Session) -> list[Location]:
    """Retrieve all locations from the database.

    Args:
        db: The database session.

    Returns:
        A list of all Location records.
    """
    logger.info('{"action": "get_all_locations"}')
    return db.query(Location).all()


def get_by_id(db: Session, location_id: int) -> Location:
    """Retrieve a single location by its primary key.

    Args:
        db: The database session.
        location_id: The primary key of the location to retrieve.

    Returns:
        The Location record with the given id.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    logger.info('{"action": "get_location_by_id", "location_id": %s}', location_id)
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


def create(db: Session, data: LocationCreate) -> Location:
    """Create a new location record.

    Args:
        db: The database session.
        data: The validated data for the new location.

    Returns:
        The newly created Location record.

    Raises:
        HTTPException: 400 if a location with the same name already exists.
    """
    logger.info('{"action": "create_location", "name": "%s"}'  , data.name)
    existing = db.query(Location).filter(Location.name == data.name).first()
    if existing is not None:
        raise HTTPException(status_code=400, detail="Location name already exists")
    location = Location(
        name=data.name,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update(db: Session, location_id: int, data: LocationUpdate) -> Location:
    """Update an existing location record.

    Only fields that are not None in ``data`` will be applied.

    Args:
        db: The database session.
        location_id: The primary key of the location to update.
        data: The validated partial update data.

    Returns:
        The updated Location record.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    logger.info('{"action": "update_location", "location_id": %s}', location_id)
    location = get_by_id(db, location_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


def delete(db: Session, location_id: int) -> None:
    """Delete a location record.

    Args:
        db: The database session.
        location_id: The primary key of the location to delete.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    logger.info('{"action": "delete_location", "location_id": %s}', location_id)
    location = get_by_id(db, location_id)
    db.delete(location)
    db.commit()
