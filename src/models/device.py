"""SQLAlchemy model for the Device resource."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base


class Device(Base):
    """Represents a physical device in the registry.

    Attributes:
        id: Primary key, auto-incremented.
        serial_number: Unique serial number of the device.
        name: Human-readable name of the device.
        device_type_id: Foreign key referencing the device_types table.
        location_id: Optional foreign key referencing the locations table.
        status: Current status of the device (default 'active').
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
        device_type: Relationship to the DeviceType model.
        location: Relationship to the Location model.
    """

    __tablename__ = "devices"

    id = __import__('sqlalchemy', fromlist=['Column']).Column(Integer, primary_key=True, autoincrement=True)
    serial_number = __import__('sqlalchemy', fromlist=['Column']).Column(String(100), unique=True, nullable=False, index=True)
    name = __import__('sqlalchemy', fromlist=['Column']).Column(String(150), nullable=False)
    device_type_id = __import__('sqlalchemy', fromlist=['Column']).Column(Integer, ForeignKey('device_types.id'), nullable=False)
    location_id = __import__('sqlalchemy', fromlist=['Column']).Column(Integer, ForeignKey('locations.id'), nullable=True)
    status = __import__('sqlalchemy', fromlist=['Column']).Column(String(50), nullable=False, default='active')
    created_at = __import__('sqlalchemy', fromlist=['Column']).Column(DateTime, default=datetime.utcnow)
    updated_at = __import__('sqlalchemy', fromlist=['Column']).Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    device_type = relationship('DeviceType', backref='devices')
    location = relationship('Location', backref='devices')
