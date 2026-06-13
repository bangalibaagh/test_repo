"""API routes for DeviceType resources.

This module defines the FastAPI router and endpoint handlers for
CRUD operations on device types.
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services import device_type_service

router = APIRouter(prefix="/device-types", tags=["device_types"])


@router.get("/", response_model=list[DeviceTypeOut], status_code=200)
def list_device_types(db: Session = Depends(get_db)):
    """Return a list of all device types.

    Args:
        db: Database session provided by dependency injection.

    Returns:
        A list of DeviceTypeOut objects.
    """
    return device_type_service.get_all(db)


@router.post("/", response_model=DeviceTypeOut, status_code=201)
def create_device_type(data: DeviceTypeCreate, db: Session = Depends(get_db)):
    """Create a new device type.

    Args:
        data: Validated request body containing device type fields.
        db: Database session provided by dependency injection.

    Returns:
        The newly created DeviceTypeOut object.
    """
    return device_type_service.create(db, data)


@router.get("/{device_type_id}", response_model=DeviceTypeOut, status_code=200)
def get_device_type(device_type_id: int, db: Session = Depends(get_db)):
    """Retrieve a device type by its ID.

    Args:
        device_type_id: Primary key of the device type to retrieve.
        db: Database session provided by dependency injection.

    Returns:
        The DeviceTypeOut object for the requested ID.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    device_type = device_type_service.get_by_id(db, device_type_id)
    if device_type is None:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type


@router.put("/{device_type_id}", response_model=DeviceTypeOut, status_code=200)
def update_device_type(
    device_type_id: int, data: DeviceTypeUpdate, db: Session = Depends(get_db)
):
    """Update an existing device type.

    Args:
        device_type_id: Primary key of the device type to update.
        data: Validated partial request body with fields to update.
        db: Database session provided by dependency injection.

    Returns:
        The updated DeviceTypeOut object.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    device_type = device_type_service.update(db, device_type_id, data)
    if device_type is None:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type


@router.delete("/{device_type_id}", status_code=204)
def delete_device_type(device_type_id: int, db: Session = Depends(get_db)):
    """Delete a device type by its ID.

    Args:
        device_type_id: Primary key of the device type to delete.
        db: Database session provided by dependency injection.

    Returns:
        An empty Response with HTTP 204 status.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    deleted = device_type_service.delete(db, device_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device type not found")
    return Response()
