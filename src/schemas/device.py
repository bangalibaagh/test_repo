"""Pydantic schemas for the Device resource."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    """Schema for creating a new device.

    Attributes:
        serial_number: Unique serial number of the device.
        name: Human-readable name of the device.
        device_type_id: ID of the associated device type.
        location_id: Optional ID of the associated location.
        status: Current status of the device.
    """

    serial_number: str
    name: str
    device_type_id: int
    location_id: Optional[int] = None
    status: str = 'active'


class DeviceUpdate(BaseModel):
    """Schema for updating an existing device.

    Attributes:
        serial_number: Optional new serial number.
        name: Optional new name.
        device_type_id: Optional new device type ID.
        location_id: Optional new location ID.
        status: Optional new status.
    """

    serial_number: Optional[str] = None
    name: Optional[str] = None
    device_type_id: Optional[int] = None
    location_id: Optional[int] = None
    status: Optional[str] = None


class DeviceOut(BaseModel):
    """Schema for returning device data in API responses.

    Attributes:
        id: Primary key of the device.
        serial_number: Unique serial number of the device.
        name: Human-readable name of the device.
        device_type_id: ID of the associated device type.
        location_id: Optional ID of the associated location.
        status: Current status of the device.
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    serial_number: str
    name: str
    device_type_id: int
    location_id: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
