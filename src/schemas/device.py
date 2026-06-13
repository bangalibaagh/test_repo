"""Pydantic schemas for the Device resource.

This module defines request and response schemas used by the device
routes and service layer.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    """Schema for creating a new device.

    Attributes:
        serial_number: Unique serial number for the device.
        name: Human-readable name for the device.
        status: Operational status, defaults to 'active'.
        device_type_id: Optional foreign key to a DeviceType record.
        location_id: Optional foreign key to a Location record.
    """

    serial_number: str
    name: str
    status: str = "active"
    device_type_id: Optional[int] = None
    location_id: Optional[int] = None


class DeviceUpdate(BaseModel):
    """Schema for updating an existing device.

    All fields are optional; only provided fields will be updated.

    Attributes:
        serial_number: New serial number for the device.
        name: New name for the device.
        status: New operational status.
        device_type_id: New foreign key to a DeviceType record.
        location_id: New foreign key to a Location record.
    """

    serial_number: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    device_type_id: Optional[int] = None
    location_id: Optional[int] = None


class DeviceOut(BaseModel):
    """Schema for serialising a device in API responses.

    Attributes:
        id: Primary key of the device record.
        serial_number: Unique serial number.
        name: Human-readable device name.
        status: Operational status string.
        device_type_id: FK to device_types, may be None.
        location_id: FK to locations, may be None.
        created_at: Timestamp when the record was created.
    """

    id: int
    serial_number: str
    name: str
    status: str
    device_type_id: Optional[int]
    location_id: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
