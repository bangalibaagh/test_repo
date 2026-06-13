"""Location routes module.

Defines the APIRouter and HTTP endpoints for the locations resource.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.location import LocationCreate, LocationOut, LocationUpdate
from src.services.location_service import (
    create_location,
    delete_location,
    get_location,
    get_locations,
    update_location,
)

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=list[LocationOut], status_code=status.HTTP_200_OK)
def list_locations(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[LocationOut]:
    """Retrieve all locations.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        db: The database session.

    Returns:
        A list of LocationOut instances.
    """
    return get_locations(db, skip=skip, limit=limit)


@router.get("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def read_location(location_id: int, db: Session = Depends(get_db)) -> LocationOut:
    """Retrieve a single location by ID.

    Args:
        location_id: The primary key of the location.
        db: The database session.

    Returns:
        The LocationOut instance.
    """
    return get_location(db, location_id)


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location_endpoint(
    data: LocationCreate, db: Session = Depends(get_db)
) -> LocationOut:
    """Create a new location.

    Args:
        data: The validated creation payload.
        db: The database session.

    Returns:
        The newly created LocationOut instance.
    """
    return create_location(db, data)


@router.put("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def update_location_endpoint(
    location_id: int, data: LocationUpdate, db: Session = Depends(get_db)
) -> LocationOut:
    """Update an existing location.

    Args:
        location_id: The primary key of the location to update.
        data: The validated update payload.
        db: The database session.

    Returns:
        The updated LocationOut instance.
    """
    return update_location(db, location_id, data)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location_endpoint(
    location_id: int, db: Session = Depends(get_db)
) -> None:
    """Delete a location by ID.

    Args:
        location_id: The primary key of the location to delete.
        db: The database session.
    """
    delete_location(db, location_id)
