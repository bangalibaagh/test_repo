"""Pydantic schemas for Location request and response validation.

This module defines the schemas used for creating, updating, and returning
Location resources through the API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    """Schema for creating a new location.

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


class LocationUpdate(BaseModel):
    """Schema for updating an existing location.

    All fields are optional; only provided fields will be updated.

    Attributes:
        name: Human-readable name for the location.
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
        name: Human-readable name for the location.
        address: Optional street address.
        latitude: Optional geographic latitude.
        longitude: Optional geographic longitude.
        created_at: Timestamp when the record was created.
    """

    id: int
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
