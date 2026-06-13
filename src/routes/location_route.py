"""API routes for the Location resource.

This module defines the FastAPI router and endpoint handlers for
CRUD operations on Location records.
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.location import LocationCreate, LocationOut, LocationUpdate
from src.services import location_service

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=list[LocationOut], status_code=200)
def list_locations(db: Session = Depends(get_db)):
    """Return all locations.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        A list of LocationOut instances.
    """
    return location_service.get_all(db)


@router.post("/", response_model=LocationOut, status_code=201)
def create_location(data: LocationCreate, db: Session = Depends(get_db)):
    """Create a new location.

    Args:
        data: Validated request body for the new location.
        db: Database session injected by FastAPI.

    Returns:
        The created LocationOut instance.
    """
    return location_service.create(db, data)


@router.get("/{location_id}", response_model=LocationOut, status_code=200)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Return a single location by ID.

    Args:
        location_id: Primary key of the location to retrieve.
        db: Database session injected by FastAPI.

    Returns:
        The matching LocationOut instance.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    location = location_service.get_by_id(db, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/{location_id}", response_model=LocationOut, status_code=200)
def update_location(location_id: int, data: LocationUpdate, db: Session = Depends(get_db)):
    """Update an existing location.

    Args:
        location_id: Primary key of the location to update.
        data: Validated partial data to apply.
        db: Database session injected by FastAPI.

    Returns:
        The updated LocationOut instance.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    location = location_service.update(db, location_id, data)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a location by ID.

    Args:
        location_id: Primary key of the location to delete.
        db: Database session injected by FastAPI.

    Returns:
        An empty Response with status 204.

    Raises:
        HTTPException: 404 if the location does not exist.
    """
    deleted = location_service.delete(db, location_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Location not found")
    return Response(status_code=204)
