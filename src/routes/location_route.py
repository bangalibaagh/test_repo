"""FastAPI router for the locations resource."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.location import LocationCreate, LocationOut, LocationUpdate
from src.services import location_service

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=list[LocationOut], status_code=status.HTTP_200_OK)
def list_locations(db: Session = Depends(get_db)) -> list[LocationOut]:
    """Return all locations.

    Args:
        db: Database session provided by dependency injection.

    Returns:
        A list of LocationOut objects.
    """
    return location_service.get_all(db)


@router.get("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def get_location(location_id: int, db: Session = Depends(get_db)) -> LocationOut:
    """Return a single location by id.

    Args:
        location_id: Primary key of the location.
        db: Database session provided by dependency injection.

    Returns:
        The matching LocationOut object.
    """
    return location_service.get_by_id(db, location_id)


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location(data: LocationCreate, db: Session = Depends(get_db)) -> LocationOut:
    """Create a new location.

    Args:
        data: Validated creation payload.
        db: Database session provided by dependency injection.

    Returns:
        The newly created LocationOut object.
    """
    return location_service.create(db, data)


@router.put("/{location_id}", response_model=LocationOut, status_code=status.HTTP_200_OK)
def update_location(
    location_id: int, data: LocationUpdate, db: Session = Depends(get_db)
) -> LocationOut:
    """Update an existing location.

    Args:
        location_id: Primary key of the location to update.
        data: Validated update payload.
        db: Database session provided by dependency injection.

    Returns:
        The updated LocationOut object.
    """
    return location_service.update(db, location_id, data)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a location.

    Args:
        location_id: Primary key of the location to delete.
        db: Database session provided by dependency injection.
    """
    location_service.delete(db, location_id)
