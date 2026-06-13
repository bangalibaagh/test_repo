"""SQLAlchemy model for the Location resource.

This module defines the Location ORM model mapped to the ``locations``
table in the application database.

Typical usage::

    from src.models.location import Location
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from src.config.database import Base


class Location(Base):
    """ORM model representing a physical location.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Unique human-readable name for the location.
        address: Optional street address.
        latitude: Optional geographic latitude.
        longitude: Optional geographic longitude.
        created_at: Timestamp when the record was created.
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
