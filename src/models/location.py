"""SQLAlchemy model for the Location resource."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from src.config.database import Base


class Location(Base):
    """SQLAlchemy ORM model representing a physical location.

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
    name = Column(String(150), unique=True, nullable=False, index=True)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
