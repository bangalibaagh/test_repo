"""API routes for the device_types resource."""

from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services import device_type_service

router = APIRouter(prefix="/device-types", tags=["device_types"])


@router.get("/", response_model=List[DeviceTypeOut], status_code=200)
def list_device_types(db: Session = Depends(get_db)) -> List[DeviceTypeOut]:
    """Return all device types.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        List of DeviceTypeOut instances.
    """
    return device_type_service.get_all(db)


@router.get("/{id}", response_model=DeviceTypeOut, status_code=200)
def get_device_type(id: int, db: Session = Depends(get_db)) -> DeviceTypeOut:
    """Return a single device type by id.

    Args:
        id: Primary key of the device type.
        db: Database session injected by FastAPI.

    Returns:
        The matching DeviceTypeOut instance.
    """
    return device_type_service.get_by_id(db, id)


@router.post("/", response_model=DeviceTypeOut, status_code=201)
def create_device_type(payload: DeviceTypeCreate, db: Session = Depends(get_db)) -> DeviceTypeOut:
    """Create a new device type.

    Args:
        payload: Validated creation payload.
        db: Database session injected by FastAPI.

    Returns:
        The newly created DeviceTypeOut instance.
    """
    return device_type_service.create(db, payload)


@router.put("/{id}", response_model=DeviceTypeOut, status_code=200)
def update_device_type(id: int, payload: DeviceTypeUpdate, db: Session = Depends(get_db)) -> DeviceTypeOut:
    """Update an existing device type.

    Args:
        id: Primary key of the device type to update.
        payload: Validated update payload.
        db: Database session injected by FastAPI.

    Returns:
        The updated DeviceTypeOut instance.
    """
    return device_type_service.update(db, id, payload)


@router.delete("/{id}", status_code=204)
def delete_device_type(id: int, db: Session = Depends(get_db)) -> Response:
    """Delete a device type by id.

    Args:
        id: Primary key of the device type to delete.
        db: Database session injected by FastAPI.

    Returns:
        Empty response with status 204.
    """
    device_type_service.delete(db, id)
    return Response(status_code=204)
