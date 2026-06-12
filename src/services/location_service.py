"""Service layer for the Location resource."""

import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
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
    logger.info("Fetching all locations")
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
    logger.info("Fetching location id=%s", location_id)
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        logger.warning("Location id=%s not found", location_id)
        raise HTTPException(status_code=404, detail="Location not found")
    return location


def create(db: Session, data: LocationCreate) -> Location:
    """Create a new location record.

    Args:
        db: The database session.
        data: The validated input data for the new location.

    Returns:
        The newly created Location record.

    Raises:
        HTTPException: 409 if a location with the same name already exists.
    """
    logger.info("Creating location name=%s", data.name)
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
        logger.warning("Duplicate location name=%s", data.name)
        raise HTTPException(status_code=409, detail="Location name already exists")
    return location


def update(db: Session, location_id: int, data: LocationUpdate) -> Location:
    """Update an existing location record.

    Args:
        db: The database session.
        location_id: The primary key of the location to update.
        data: The validated input data with fields to update.

    Returns:
        The updated Location record.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    logger.info("Updating location id=%s", location_id)
    location = get_by_id(db, location_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


def delete(db: Session, location_id: int) -> None:
    """Delete a location record by its primary key.

    Args:
        db: The database session.
        location_id: The primary key of the location to delete.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    logger.info("Deleting location id=%s", location_id)
    location = get_by_id(db, location_id)
    db.delete(location)
    db.commit()
