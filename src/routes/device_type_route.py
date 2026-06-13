"""Routes for the device-types resource.

Registers five CRUD endpoints under the /device-types prefix.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services.device_type_service import (
    create_device_type as svc_create,
    delete_device_type as svc_delete,
    get_device_type as svc_get,
    get_device_types as svc_list,
    update_device_type as svc_update,
)

router = APIRouter(prefix="/device-types", tags=["device-types"])


@router.get("/", response_model=list[DeviceTypeOut], status_code=status.HTTP_200_OK)
def list_device_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[DeviceTypeOut]:
    """List all device types.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        db: Injected database session.

    Returns:
        A list of device type objects.
    """
    return svc_list(db, skip=skip, limit=limit)


@router.post("/", response_model=DeviceTypeOut, status_code=status.HTTP_201_CREATED)
def create_device_type(
    data: DeviceTypeCreate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Create a new device type.

    Args:
        data: The creation payload.
        db: Injected database session.

    Returns:
        The newly created device type.
    """
    return svc_create(db, data)


@router.get(
    "/{device_type_id}", response_model=DeviceTypeOut, status_code=status.HTTP_200_OK
)
def get_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Retrieve a device type by ID.

    Args:
        device_type_id: The primary key of the device type.
        db: Injected database session.

    Returns:
        The matching device type.
    """
    return svc_get(db, device_type_id)


@router.put(
    "/{device_type_id}", response_model=DeviceTypeOut, status_code=status.HTTP_200_OK
)
def update_device_type(
    device_type_id: int, data: DeviceTypeUpdate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Update an existing device type.

    Args:
        device_type_id: The primary key of the device type to update.
        data: The update payload.
        db: Injected database session.

    Returns:
        The updated device type.
    """
    return svc_update(db, device_type_id, data)


@router.delete(
    "/{device_type_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> None:
    """Delete a device type by ID.

    Args:
        device_type_id: The primary key of the device type to delete.
        db: Injected database session.

    Returns:
        None
    """
    svc_delete(db, device_type_id)
