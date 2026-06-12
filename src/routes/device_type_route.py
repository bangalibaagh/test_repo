"""FastAPI router for device_types CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.device_type import DeviceTypeCreate, DeviceTypeOut, DeviceTypeUpdate
from src.services import device_type_service

router = APIRouter(prefix="/device-types", tags=["device_types"])


@router.post("/", response_model=DeviceTypeOut, status_code=status.HTTP_201_CREATED)
def create_device_type(
    data: DeviceTypeCreate, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Create a new device type.

    Args:
        data: The request body containing device type fields.
        db: The injected SQLAlchemy database session.

    Returns:
        The newly created device type.

    Raises:
        HTTPException: 400 if a device type with the same name already exists.
    """
    try:
        return device_type_service.create(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A device type with that name already exists.",
        )


@router.get("/", response_model=list[DeviceTypeOut], status_code=status.HTTP_200_OK)
def list_device_types(db: Session = Depends(get_db)) -> list[DeviceTypeOut]:
    """Retrieve all device types.

    Args:
        db: The injected SQLAlchemy database session.

    Returns:
        A list of all device types.
    """
    return device_type_service.get_all(db)


@router.get(
    "/{device_type_id}",
    response_model=DeviceTypeOut,
    status_code=status.HTTP_200_OK,
)
def get_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> DeviceTypeOut:
    """Retrieve a single device type by ID.

    Args:
        device_type_id: The integer primary key of the device type.
        db: The injected SQLAlchemy database session.

    Returns:
        The matching device type.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    device_type = device_type_service.get_by_id(db, device_type_id)
    if device_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device type not found.",
        )
    return device_type


@router.put(
    "/{device_type_id}",
    response_model=DeviceTypeOut,
    status_code=status.HTTP_200_OK,
)
def update_device_type(
    device_type_id: int,
    data: DeviceTypeUpdate,
    db: Session = Depends(get_db),
) -> DeviceTypeOut:
    """Update an existing device type.

    Args:
        device_type_id: The integer primary key of the device type to update.
        data: The request body containing fields to update.
        db: The injected SQLAlchemy database session.

    Returns:
        The updated device type.

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    device_type = device_type_service.update(db, device_type_id, data)
    if device_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device type not found.",
        )
    return device_type


@router.delete("/{device_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_type(
    device_type_id: int, db: Session = Depends(get_db)
) -> None:
    """Delete a device type by ID.

    Args:
        device_type_id: The integer primary key of the device type to delete.
        db: The injected SQLAlchemy database session.

    Returns:
        None

    Raises:
        HTTPException: 404 if the device type is not found.
    """
    deleted = device_type_service.delete(db, device_type_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device type not found.",
        )
