"""Location schema module.

Defines Pydantic models for request validation and response serialization
of the locations resource.
"""

from pydantic import BaseModel


class LocationCreate(BaseModel):
    """Schema for creating a new location.

    Attributes:
        name: The name of the location.
        address: Optional address of the location.
        description: Optional description of the location.
    """

    name: str
    address: str | None = None
    description: str | None = None


class LocationUpdate(BaseModel):
    """Schema for updating an existing location.

    All fields are optional so partial updates are supported.

    Attributes:
        name: Optional new name for the location.
        address: Optional new address for the location.
        description: Optional new description for the location.
    """

    name: str | None = None
    address: str | None = None
    description: str | None = None


class LocationOut(BaseModel):
    """Schema for serializing a location in responses.

    Attributes:
        id: The unique identifier of the location.
        name: The name of the location.
        address: The address of the location.
        description: The description of the location.
    """

    id: int
    name: str
    address: str | None
    description: str | None

    model_config = {"from_attributes": True}
