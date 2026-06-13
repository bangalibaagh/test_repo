"""FastAPI router for the Location resource.

This module registers all HTTP endpoints for creating, reading,
updating, and deleting Location records.

Typical usage::

    from src.routes.location_route import router
    app.include_router(router)
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.location import LocationCreate, LocationOut, LocationUpdate
from src.services import location_service

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=List[LocationOut], status_code=status.HTTP_200_OK)
def list_locations(db: Session = Depends(get_db)) -> List[LocationOut]:
    """Return all locations.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        List of all location records.
    """
    return location_service.get_all(db)


@router.get("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def get_location(location_id: int, db: Session = Depends(get_db)) -> LocationOut:
    """Return a single location by id.

    Args:
        location_id: Primary key of the location.
        db: Database session injected by FastAPI.

    Returns:
        The matching location record.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    return location_service.get_by_id(location_id, db)


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location(data: LocationCreate, db: Session = Depends(get_db)) -> LocationOut:
    """Create a new location.

    Args:
        data: Validated location creation payload.
        db: Database session injected by FastAPI.

    Returns:
        The newly created location record.

    Raises:
        HTTPException: 409 if a location with the same name already exists.
    """
    return location_service.create(data, db)


@router.put("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def update_location(
    location_id: int, data: LocationUpdate, db: Session = Depends(get_db)
) -> LocationOut:
    """Update an existing location.

    Args:
        location_id: Primary key of the location to update.
        data: Validated partial update payload.
        db: Database session injected by FastAPI.

    Returns:
        The updated location record.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    return location_service.update(location_id, data, db)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a location by id.

    Args:
        location_id: Primary key of the location to delete.
        db: Database session injected by FastAPI.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    location_service.delete(location_id, db)
