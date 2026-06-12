"""Pydantic schemas for the Location resource."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    """Schema for creating a new location.

    Attributes:
        name: Unique human-readable name for the location.
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

    All fields are optional so partial updates are supported.

    Attributes:
        name: Updated name for the location.
        address: Updated street address.
        latitude: Updated geographic latitude.
        longitude: Updated geographic longitude.
    """

    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationOut(BaseModel):
    """Schema for serialising a location in API responses.

    Attributes:
        id: Primary key of the location record.
        name: Human-readable name for the location.
        address: Street address of the location.
        latitude: Geographic latitude.
        longitude: Geographic longitude.
        created_at: Timestamp when the record was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime
