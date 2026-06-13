"""SQLAlchemy model for DeviceType.

This module defines the DeviceType ORM model mapped to the device_types table.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.config.database import Base


class DeviceType(Base):
    """ORM model representing a device type.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Unique, non-nullable string identifier (max 100 chars).
        description: Optional description string (max 255 chars).
        created_at: Timestamp of record creation, defaults to utcnow.
    """

    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
