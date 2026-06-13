"""Business logic for the Location resource.

This module provides service functions that interact with the database
for CRUD operations on Location records.
"""

import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate

logger = logging.getLogger(__name__)


def get_all(db: Session) -> List[Location]:
    """Retrieve all Location records.

    Args:
        db: Active SQLAlchemy database session.

    Returns:
        A list of all Location ORM instances.
    """
    locations = db.query(Location).all()
    logger.info({"action": "get_all_locations", "count": len(locations)})
    return locations


def get_by_id(db: Session, location_id: int) -> Optional[Location]:
    """Retrieve a single Location by its primary key.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to retrieve.

    Returns:
        The Location ORM instance if found, otherwise None.
    """
    location = db.query(Location).filter(Location.id == location_id).first()
    logger.info({"action": "get_location_by_id", "location_id": location_id, "found": location is not None})
    return location


def create(db: Session, data: LocationCreate) -> Location:
    """Create a new Location record.

    Args:
        db: Active SQLAlchemy database session.
        data: Validated data for the new location.

    Returns:
        The newly created Location ORM instance.
    """
    location = Location(**data.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    logger.info({"action": "create_location", "location_id": location.id, "name": location.name})
    return location


def update(db: Session, location_id: int, data: LocationUpdate) -> Optional[Location]:
    """Update an existing Location record.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to update.
        data: Validated partial data to apply.

    Returns:
        The updated Location ORM instance if found, otherwise None.
    """
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        logger.info({"action": "update_location", "location_id": location_id, "found": False})
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    logger.info({"action": "update_location", "location_id": location_id, "found": True})
    return location


def delete(db: Session, location_id: int) -> bool:
    """Delete a Location record by its primary key.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to delete.

    Returns:
        True if the record was deleted, False if it was not found.
    """
    location = db.query(Location).filter(Location.id == location_id).first()
    logger.info({"action": "delete_location", "location_id": location_id, "found": location is not None})
    if location is None:
        return False
    db.delete(location)
    db.commit()
    return True
