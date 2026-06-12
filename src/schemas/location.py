"""Pydantic schemas for the Location resource."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    """Schema for creating a new location.

    Attributes:
        name: Unique name of the location.
        address: Optional street address.
        latitude: Optional geographic latitude.
        longitude: Optional geographic longitude.
    """

    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationUpdate(BaseModel):
    """Schema for updating an existing location.

    All fields are optional; only provided fields will be updated.

    Attributes:
        name: Unique name of the location.
        address: Optional street address.
        latitude: Optional geographic latitude.
        longitude: Optional geographic longitude.
    """

    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationOut(BaseModel):
    """Schema for returning a location in API responses.

    Attributes:
        id: Primary key of the location.
        name: Unique name of the location.
        address: Optional street address.
        latitude: Optional geographic latitude.
        longitude: Optional geographic longitude.
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    updated_at: datetime
