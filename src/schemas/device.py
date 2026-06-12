"""Pydantic schemas for Device."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    """Base schema for Device with shared fields.

    Attributes:
        serial_number: Unique serial number of the device.
        name: Human-readable name of the device.
        status: Current status, defaults to 'active'.
        device_type_id: ID of the associated device type.
        location_id: Optional ID of the associated location.
    """

    serial_number: str
    name: str
    status: str = "active"
    device_type_id: int
    location_id: Optional[int] = None


class DeviceCreate(DeviceBase):
    """Schema for creating a new Device.

    Inherits all fields from DeviceBase.
    """


class DeviceUpdate(BaseModel):
    """Schema for updating an existing Device.

    All fields are optional to allow partial updates.

    Attributes:
        serial_number: Optional new serial number.
        name: Optional new name.
        status: Optional new status.
        device_type_id: Optional new device type ID.
        location_id: Optional new location ID.
    """

    serial_number: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    device_type_id: Optional[int] = None
    location_id: Optional[int] = None


class DeviceOut(DeviceBase):
    """Schema for returning a Device in API responses.

    Attributes:
        id: Primary key of the device.
        created_at: Timestamp when the device was created.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
