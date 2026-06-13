"""Pydantic schemas for DeviceType.

This module defines the request and response schemas used by the
device_types endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceTypeCreate(BaseModel):
    """Schema for creating a new DeviceType.

    Attributes:
        name: The unique name of the device type.
        description: An optional description of the device type.
    """

    name: str
    description: Optional[str] = None


class DeviceTypeUpdate(BaseModel):
    """Schema for updating an existing DeviceType.

    Attributes:
        name: Optional new name for the device type.
        description: Optional new description for the device type.
    """

    name: Optional[str] = None
    description: Optional[str] = None


class DeviceTypeOut(BaseModel):
    """Schema for returning a DeviceType in API responses.

    Attributes:
        id: The primary key of the device type.
        name: The unique name of the device type.
        description: An optional description of the device type.
        created_at: The timestamp when the record was created.
    """

    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
