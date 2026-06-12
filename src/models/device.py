"""SQLAlchemy model for Device."""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base


class Device(Base):
    """SQLAlchemy model representing a device.

    Attributes:
        id: Primary key, auto-incremented integer.
        serial_number: Unique serial number string, not null.
        name: Human-readable device name, not null.
        status: Current status string, defaults to 'active'.
        device_type_id: Foreign key referencing device_types.id, not null.
        location_id: Foreign key referencing locations.id, nullable.
        created_at: Timestamp of record creation.
        device_type: Relationship to DeviceType model.
        location: Relationship to Location model.
    """

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    status = Column(String(50), default="active")
    device_type_id = Column(Integer, ForeignKey("device_types.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    device_type = relationship("DeviceType")
    location = relationship("Location")
