"""SQLAlchemy model for the Device resource."""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base


class Device(Base):
    """SQLAlchemy ORM model representing a device.

    Attributes:
        id: Primary key, auto-incremented integer.
        serial_number: Unique serial number string, indexed.
        name: Human-readable name for the device.
        device_type_id: Foreign key referencing device_types.id.
        location_id: Optional foreign key referencing locations.id.
        status: Current status string, defaults to 'active'.
        created_at: Timestamp of record creation.
        device_type: Relationship to DeviceType model.
        location: Relationship to Location model.
    """

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    device_type_id = Column(Integer, ForeignKey("device_types.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    device_type = relationship("DeviceType")
    location = relationship("Location")
