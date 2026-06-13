"""SQLAlchemy model for the Location resource.

This module defines the Location ORM model mapped to the ``locations``
table in the relational database.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

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
        updated_at: Timestamp when the record was last updated.
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    address = Column(String(500), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
