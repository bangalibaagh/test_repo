"""Pydantic schemas for the Location resource.

This module defines the request and response schemas used by the
locations API endpoints.

Typical usage::

    from src.schemas.location import LocationCreate, LocationOut
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    """Shared fields for Location schemas.

    Attributes:
        name: Human-readable name for the location.
        address: Optional street address.
        latitude: Optional geographic latitude.
        longitude: Optional geographic longitude.
    """

    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationCreate(LocationBase):
    """Schema for creating a new Location.

    Inherits all fields from LocationBase.
    """


class LocationUpdate(BaseModel):
    """Schema for updating an existing Location.

    All fields are optional so partial updates are supported.

    Attributes:
        name: Updated name.
        address: Updated address.
        latitude: Updated latitude.
        longitude: Updated longitude.
    """

    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationOut(LocationBase):
    """Schema for returning a Location in API responses.

    Attributes:
        id: Primary key of the location.
        created_at: Timestamp when the location was created.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
