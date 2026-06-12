"""FastAPI router for the locations resource."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.location import LocationCreate, LocationOut, LocationUpdate
from src.services import location_service

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location(data: LocationCreate, db: Session = Depends(get_db)) -> LocationOut:
    """Create a new location.

    Args:
        data: Validated request body containing location fields.
        db: Database session injected by FastAPI.

    Returns:
        The newly created location.

    Raises:
        HTTPException: 400 if a location with the same name already exists.
    """
    try:
        return location_service.create(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A location with that name already exists.",
        )


@router.get("/", response_model=List[LocationOut], status_code=status.HTTP_200_OK)
def list_locations(db: Session = Depends(get_db)) -> List[LocationOut]:
    """Return all locations.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        A list of all location records.
    """
    return location_service.get_all(db)


@router.get("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def get_location(location_id: int, db: Session = Depends(get_db)) -> LocationOut:
    """Return a single location by ID.

    Args:
        location_id: Primary key of the location.
        db: Database session injected by FastAPI.

    Returns:
        The matching location record.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    location = location_service.get_by_id(db, location_id)
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found.",
        )
    return location


@router.put("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def update_location(
    location_id: int, data: LocationUpdate, db: Session = Depends(get_db)
) -> LocationOut:
    """Update an existing location.

    Args:
        location_id: Primary key of the location to update.
        data: Fields to update.
        db: Database session injected by FastAPI.

    Returns:
        The updated location record.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    location = location_service.update(db, location_id, data)
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found.",
        )
    return location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a location.

    Args:
        location_id: Primary key of the location to delete.
        db: Database session injected by FastAPI.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    deleted = location_service.delete(db, location_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found.",
        )
