"""Pydantic schemas for DeviceType request and response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceTypeBase(BaseModel):
    """Base schema shared by create and response schemas.

    Attributes:
        name: The name of the device type.
        description: An optional description of the device type.
    """

    name: str
    description: Optional[str] = None


class DeviceTypeCreate(DeviceTypeBase):
    """Schema for creating a new DeviceType.

    Inherits all fields from DeviceTypeBase.
    """


class DeviceTypeUpdate(BaseModel):
    """Schema for partially updating an existing DeviceType.

    Attributes:
        name: Optional new name for the device type.
        description: Optional new description for the device type.
    """

    name: Optional[str] = None
    description: Optional[str] = None


class DeviceTypeOut(DeviceTypeBase):
    """Schema for returning a DeviceType in API responses.

    Attributes:
        id: The unique identifier of the device type.
        created_at: The timestamp when the device type was created.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
