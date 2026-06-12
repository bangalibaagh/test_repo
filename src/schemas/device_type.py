"""Pydantic schemas for DeviceType."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceTypeCreate(BaseModel):
    """Schema for creating a new device type.

    Attributes:
        name: Name of the device type.
        description: Optional description of the device type.
    """

    name: str
    description: Optional[str] = None


class DeviceTypeUpdate(BaseModel):
    """Schema for updating an existing device type.

    Attributes:
        name: Optional new name for the device type.
        description: Optional new description for the device type.
    """

    name: Optional[str] = None
    description: Optional[str] = None


class DeviceTypeOut(BaseModel):
    """Schema for returning a device type in API responses.

    Attributes:
        id: Primary key of the device type.
        name: Name of the device type.
        description: Optional description of the device type.
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
