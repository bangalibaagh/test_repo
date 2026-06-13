"""Location service module.

Implements CRUD business logic for the locations resource with JSON-logged
operations and HTTPException handling.
"""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate

logger = logging.getLogger(__name__)


def get_locations(db: Session, skip: int = 0, limit: int = 100) -> list[Location]:
    """Retrieve a list of locations.

    Args:
        db: The database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of Location ORM instances.
    """
    logger.info({"action": "get_locations", "skip": skip, "limit": limit})
    return db.query(Location).offset(skip).limit(limit).all()


def get_location(db: Session, location_id: int) -> Location:
    """Retrieve a single location by ID.

    Args:
        db: The database session.
        location_id: The primary key of the location.

    Returns:
        The Location ORM instance.

    Raises:
        HTTPException: 404 if the location is not found.
    """
    logger.info({"action": "get_location", "location_id": location_id})
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


def create_location(db: Session, data: LocationCreate) -> Location:
    """Create a new location.

    Args:
        db: The database session.
        data: The validated creation payload.

    Returns:
        The newly created Location ORM instance.
    """
    logger.info({"action": "create_location", "name": data.name})
    location = Location(
        name=data.name,
        address=data.address,
        description=data.description,
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(db: Session, location_id: int, data: LocationUpdate) -> Location:
    """Update an existing location.

    Args:
        db: The database session.
        location_id: The primary key of the location to update.
        data: The validated update payload.

    Returns:
        The updated Location ORM instance.

    Raises:
        HTTPException: 404 if the location is not found.
    """
    logger.info({"action": "update_location", "location_id": location_id})
    location = get_location(db, location_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


def delete_location(db: Session, location_id: int) -> None:
    """Delete a location by ID.

    Args:
        db: The database session.
        location_id: The primary key of the location to delete.

    Raises:
        HTTPException: 404 if the location is not found.
    """
    logger.info({"action": "delete_location", "location_id": location_id})
    location = get_location(db, location_id)
    db.delete(location)
    db.commit()
