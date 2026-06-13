"""Business logic layer for the Location resource.

This module provides CRUD helper functions used by the location routes.
All database interactions are performed through the supplied SQLAlchemy
session. HTTPException is raised for client-facing error conditions.
"""

import logging
import json
from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_object["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_object)


def _get_logger(name: str) -> logging.Logger:
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


logger = _get_logger(__name__)


def get_all(db: Session) -> List[Location]:
    """Retrieve all location records.

    Args:
        db: Active SQLAlchemy database session.

    Returns:
        A list of Location ORM instances.
    """
    logger.info("Fetching all locations")
    return db.query(Location).all()


def get_by_id(db: Session, location_id: int) -> Location:
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
    if not location:
        logger.warning("Location not found with id %s", location_id)
        raise HTTPException(status_code=404, detail="Location not found")
    return location


def create(db: Session, data: LocationCreate) -> Location:
    """Create a new location record.

    Args:
        db: Active SQLAlchemy database session.
        data: Validated creation payload.

    Returns:
        The newly created Location ORM instance.

    Raises:
        HTTPException: 400 if the name is already in use.
    """
    existing = db.query(Location).filter(Location.name == data.name).first()
    if existing:
        logger.warning("Duplicate location name: %s", data.name)
        raise HTTPException(status_code=400, detail="Location name already in use")

    location = Location(
        name=data.name,
        address=getattr(data, "address", None),
        latitude=getattr(data, "latitude", None),
        longitude=getattr(data, "longitude", None),
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    logger.info("Created location with id %s", location.id)
    return location


def update(db: Session, location_id: int, data: LocationUpdate) -> Location:
    """Update an existing location record.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to update.
        data: Validated update payload.

    Returns:
        The updated Location ORM instance.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = get_by_id(db, location_id)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)

    db.commit()
    db.refresh(location)
    logger.info("Updated location with id %s", location_id)
    return location


def delete(db: Session, location_id: int) -> None:
    """Delete a location record.

    Args:
        db: Active SQLAlchemy database session.
        location_id: Primary key of the location to delete.

    Raises:
        HTTPException: 404 if no location with the given id exists.
    """
    location = get_by_id(db, location_id)
    db.delete(location)
    db.commit()
    logger.info("Deleted location with id %s", location_id)
