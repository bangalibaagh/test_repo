"""Pydantic v2 schemas for DeviceType.

This module defines request and response schemas used by the device_types
API endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceTypeBase(BaseModel):
    """Shared fields for DeviceType schemas.

    Attributes:
        name: Name of the device type.
        description: Optional description of the device type.
    """

    name: str
    description: Optional[str] = None


class DeviceTypeCreate(DeviceTypeBase):
    """Schema for creating a new DeviceType.

    Inherits all fields from DeviceTypeBase with no additional fields.
    """


class DeviceTypeUpdate(BaseModel):
    """Schema for updating an existing DeviceType.

    Attributes:
        name: Optional new name for the device type.
        description: Optional new description for the device type.
    """

    name: Optional[str] = None
    description: Optional[str] = None


class DeviceTypeOut(DeviceTypeBase):
    """Schema for returning a DeviceType in API responses.

    Attributes:
        id: Primary key of the device type.
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
