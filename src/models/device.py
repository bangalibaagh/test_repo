"""SQLAlchemy model for the Device resource.

This module defines the Device ORM model with foreign key relationships
to the device_types and locations tables.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base


class Device(Base):
    """ORM model representing a physical or virtual device.

    Attributes:
        id: Primary key, auto-incremented integer.
        serial_number: Unique serial number string, not nullable.
        name: Human-readable device name, not nullable.
        status: Operational status string, defaults to 'active'.
        device_type_id: Optional FK to device_types.id.
        location_id: Optional FK to locations.id.
        created_at: Timestamp of record creation.
        device_type: Relationship to DeviceType model.
        location: Relationship to Location model.
    """

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    status = Column(String(50), default="active")
    device_type_id = Column(Integer, ForeignKey("device_types.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    device_type = relationship("DeviceType", back_populates=None, lazy="joined")
    location = relationship("Location", back_populates=None, lazy="joined")
