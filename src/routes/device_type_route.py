"""FastAPI routes for the device_types resource."""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services.device_type_service import (
    create_device_type,
    delete_device_type,
    get_device_type,
    get_device_types,
    update_device_type,
)

router = APIRouter(prefix="/device-types", tags=["device_types"])


@router.get("/", response_model=list[DeviceTypeOut], status_code=200)
def list_device_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all device types.

    Args:
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        db: Database session injected by FastAPI.

    Returns:
        A list of DeviceTypeOut objects.
    """
    return get_device_types(db, skip=skip, limit=limit)


@router.post("/", response_model=DeviceTypeOut, status_code=201)
def create_device_type_endpoint(data: DeviceTypeCreate, db: Session = Depends(get_db)):
    """Create a new device type.

    Args:
        data: Request body containing the device type fields.
        db: Database session injected by FastAPI.

    Returns:
        The created DeviceTypeOut object.
    """
    return create_device_type(db, data)


@router.get("/{device_type_id}", response_model=DeviceTypeOut, status_code=200)
def get_device_type_endpoint(device_type_id: int, db: Session = Depends(get_db)):
    """Retrieve a device type by ID.

    Args:
        device_type_id: Primary key of the device type.
        db: Database session injected by FastAPI.

    Returns:
        The DeviceTypeOut object if found.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    device_type = get_device_type(db, device_type_id)
    if device_type is None:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type


@router.put("/{device_type_id}", response_model=DeviceTypeOut, status_code=200)
def update_device_type_endpoint(device_type_id: int, data: DeviceTypeUpdate, db: Session = Depends(get_db)):
    """Update an existing device type.

    Args:
        device_type_id: Primary key of the device type to update.
        data: Request body containing the fields to update.
        db: Database session injected by FastAPI.

    Returns:
        The updated DeviceTypeOut object.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    device_type = update_device_type(db, device_type_id, data)
    if device_type is None:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type


@router.delete("/{device_type_id}", status_code=204)
def delete_device_type_endpoint(device_type_id: int, db: Session = Depends(get_db)):
    """Delete a device type by ID.

    Args:
        device_type_id: Primary key of the device type to delete.
        db: Database session injected by FastAPI.

    Returns:
        An empty Response with status 204 on success.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    deleted = delete_device_type(db, device_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device type not found")
    return Response()
