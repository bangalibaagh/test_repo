"""SQLAlchemy model for the locations resource."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from src.config.database import Base


class Location(Base):
    """SQLAlchemy model representing a physical location.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Unique name of the location, indexed.
        address: Optional street address.
        latitude: Optional geographic latitude.
        longitude: Optional geographic longitude.
        created_at: Timestamp when the record was created.
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    address = Column(String(300), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
