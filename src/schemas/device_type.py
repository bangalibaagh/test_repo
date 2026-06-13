"""Pydantic schemas for the device_types resource.

Defines request and response models used by the device-types endpoints.
"""

from pydantic import BaseModel, ConfigDict


class DeviceTypeCreate(BaseModel):
    """Schema for creating a new device type.

    Attributes:
        name: The name of the device type.
        description: An optional description of the device type.
    """

    name: str
    description: str | None = None


class DeviceTypeUpdate(BaseModel):
    """Schema for updating an existing device type.

    Attributes:
        name: The new name of the device type, if updating.
        description: The new description of the device type, if updating.
    """

    name: str | None = None
    description: str | None = None


class DeviceTypeOut(BaseModel):
    """Schema for returning a device type in API responses.

    Attributes:
        id: The unique identifier of the device type.
        name: The name of the device type.
        description: An optional description of the device type.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
