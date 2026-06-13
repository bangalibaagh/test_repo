"""Device schema module.

Defines Pydantic schemas for device request validation and response serialization.
"""

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    """Schema for creating a new device.

    Attributes:
        name: Human-readable name of the device.
        serial_number: Optional unique serial number.
        device_type_id: ID of the associated device type.
        location_id: Optional ID of the associated location.
    """

    name: str
    serial_number: str | None = None
    device_type_id: int
    location_id: int | None = None


class DeviceUpdate(BaseModel):
    """Schema for updating an existing device.

    All fields are optional; only provided fields will be updated.

    Attributes:
        name: Human-readable name of the device.
        serial_number: Optional unique serial number.
        device_type_id: ID of the associated device type.
        location_id: Optional ID of the associated location.
    """

    name: str | None = None
    serial_number: str | None = None
    device_type_id: int | None = None
    location_id: int | None = None


class DeviceOut(BaseModel):
    """Schema for serializing a device in API responses.

    Attributes:
        id: Primary key of the device.
        name: Human-readable name of the device.
        serial_number: Optional unique serial number.
        device_type_id: ID of the associated device type.
        location_id: Optional ID of the associated location.
    """

    id: int
    name: str
    serial_number: str | None
    device_type_id: int
    location_id: int | None

    model_config = {"from_attributes": True}
