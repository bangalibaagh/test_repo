"""FastAPI router for Location endpoints.

This module defines the API routes for creating, reading, updating,
and deleting Location resources.
"""

from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dependencies.auth import require_api_key
from src.schemas.location import LocationCreate, LocationOut, LocationUpdate
from src.services import location_service

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=List[LocationOut], status_code=200)
def list_locations(db: Session = Depends(get_db)) -> List[LocationOut]:
    """List all locations.

    Args:
        db: The database session provided by dependency injection.

    Returns:
        A list of all LocationOut records.
    """
    return location_service.get_all(db)


@router.post("/", response_model=LocationOut, status_code=201)
def create_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
) -> LocationOut:
    """Create a new location.

    Args:
        data: The validated request body for the new location.
        db: The database session provided by dependency injection.

    Returns:
        The newly created LocationOut record.
    """
    return location_service.create(db, data)


@router.get("/{location_id}", response_model=LocationOut, status_code=200)
def get_location(
    location_id: int, db: Session = Depends(get_db)
) -> LocationOut:
    """Retrieve a single location by id.

    Args:
        location_id: The primary key of the location to retrieve.
        db: The database session provided by dependency injection.

    Returns:
        The LocationOut record for the given id.
    """
    return location_service.get_by_id(db, location_id)


@router.put("/{location_id}", response_model=LocationOut, status_code=200)
def update_location(
    location_id: int,
    data: LocationUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
) -> LocationOut:
    """Update an existing location.

    Args:
        location_id: The primary key of the location to update.
        data: The validated partial update data.
        db: The database session provided by dependency injection.

    Returns:
        The updated LocationOut record.
    """
    return location_service.update(db, location_id, data)


@router.delete("/{location_id}", status_code=204)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
) -> Response:
    """Delete a location by id.

    Args:
        location_id: The primary key of the location to delete.
        db: The database session provided by dependency injection.

    Returns:
        An empty response with HTTP 204 status.
    """
    location_service.delete(db, location_id)
    return Response(status_code=204)
