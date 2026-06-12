"""FastAPI router for the Location resource."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.location import LocationCreate, LocationOut, LocationUpdate
from src.services.location_service import (
    create_location,
    delete_location,
    get_location,
    list_locations,
    update_location,
)

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location_endpoint(
    payload: LocationCreate, db: Session = Depends(get_db)
) -> LocationOut:
    """Create a new location.

    Args:
        payload: Validated request body containing location data.
        db: Injected database session.

    Returns:
        The newly created location serialised as LocationOut.
    """
    return create_location(db, payload)


@router.get("/", response_model=List[LocationOut], status_code=status.HTTP_200_OK)
def list_locations_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[LocationOut]:
    """Return a paginated list of locations.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        db: Injected database session.

    Returns:
        A list of locations serialised as LocationOut.
    """
    return list_locations(db, skip=skip, limit=limit)


@router.get("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def get_location_endpoint(
    location_id: int, db: Session = Depends(get_db)
) -> LocationOut:
    """Retrieve a single location by id.

    Args:
        location_id: Primary key of the location to retrieve.
        db: Injected database session.

    Returns:
        The matching location serialised as LocationOut.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    return get_location(db, location_id)


@router.put("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def update_location_endpoint(
    location_id: int, payload: LocationUpdate, db: Session = Depends(get_db)
) -> LocationOut:
    """Partially update an existing location.

    Args:
        location_id: Primary key of the location to update.
        payload: Fields to update.
        db: Injected database session.

    Returns:
        The updated location serialised as LocationOut.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    return update_location(db, location_id, payload)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location_endpoint(
    location_id: int, db: Session = Depends(get_db)
) -> None:
    """Delete a location by id.

    Args:
        location_id: Primary key of the location to delete.
        db: Injected database session.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    delete_location(db, location_id)
