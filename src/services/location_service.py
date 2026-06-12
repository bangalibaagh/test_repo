"""Service layer for the Location resource."""

import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate

logger = logging.getLogger(__name__)


def create_location(db: Session, payload: LocationCreate) -> Location:
    """Persist a new location record.

    Args:
        db: Active SQLAlchemy database session.
        payload: Validated data for the new location.

    Returns:
        The newly created Location ORM instance.
    """
    location = Location(
        name=payload.name,
        address=payload.address,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    logger.info(
        "location_created",
        extra={"event": "location_created", "id": location.id, "name": location.name},
    )
    return location


def get_location(db: Session, location_id: int) -> Location:
    """Retrieve a single location by primary key.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to retrieve.

    Returns:
        The matching Location ORM instance.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        logger.warning(
            "location_not_found",
            extra={"event": "location_not_found", "id": location_id},
        )
        raise HTTPException(status_code=404, detail="Location not found")
    return location


def list_locations(db: Session, skip: int = 0, limit: int = 100) -> List[Location]:
    """Return a paginated list of locations.

    Args:
        db: Active SQLAlchemy database session.
        skip: Number of records to skip (offset).
        limit: Maximum number of records to return.

    Returns:
        A list of Location ORM instances.
    """
    return db.query(Location).offset(skip).limit(limit).all()


def update_location(db: Session, location_id: int, payload: LocationUpdate) -> Location:
    """Apply a partial update to an existing location.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to update.
        payload: Fields to update; unset fields are left unchanged.

    Returns:
        The updated Location ORM instance.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = get_location(db, location_id)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    logger.info(
        "location_updated",
        extra={"event": "location_updated", "id": location.id},
    )
    return location


def delete_location(db: Session, location_id: int) -> None:
    """Delete an existing location.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to delete.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = get_location(db, location_id)
    db.delete(location)
    db.commit()
    logger.info(
        "location_deleted",
        extra={"event": "location_deleted", "id": location_id},
    )
