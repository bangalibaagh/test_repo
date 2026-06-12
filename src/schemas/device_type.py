"""Pydantic schemas for device type input and output."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceTypeCreate(BaseModel):
    """Schema for creating a new device type.

    Attributes:
        name: The name of the device type.
        description: An optional description of the device type.
    """

    name: str
    description: Optional[str] = None


class DeviceTypeUpdate(BaseModel):
    """Schema for partially updating an existing device type.

    Attributes:
        name: Optional new name for the device type.
        description: Optional new description for the device type.
    """

    name: Optional[str] = None
    description: Optional[str] = None


class DeviceTypeOut(BaseModel):
    """Schema for returning device type data in responses.

    Attributes:
        id: The unique identifier of the device type.
        name: The name of the device type.
        description: An optional description of the device type.
        created_at: The timestamp when the device type was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime
