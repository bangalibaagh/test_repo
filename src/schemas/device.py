"""Pydantic schemas for the Device resource.

This module defines request and response schemas used by the devices
API endpoints.

Typical usage::

    from src.schemas.device import DeviceCreate, DeviceOut
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    """Shared fields for Device schemas.

    Attributes:
        serial_number: Unique serial number of the device.
        name: Human-readable name of the device.
        device_type_id: ID of the associated device type.
        location_id: Optional ID of the associated location.
        status: Current status of the device, defaults to 'active'.
    """

    serial_number: str
    name: str
    device_type_id: int
    location_id: Optional[int] = None
    status: str = "active"


class DeviceCreate(DeviceBase):
    """Schema for creating a new Device."""


class DeviceUpdate(BaseModel):
    """Schema for updating an existing Device.

    All fields are optional so partial updates are supported.

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


class DeviceOut(DeviceBase):
    """Schema for returning a Device in API responses.

    Attributes:
        id: Primary key of the device record.
        created_at: Timestamp when the record was created.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
