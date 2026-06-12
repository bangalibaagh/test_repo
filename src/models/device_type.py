"""SQLAlchemy model for DeviceType."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.config.database import Base


class DeviceType(Base):
    """Represents a device type in the database.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Unique name of the device type, max 100 characters.
        description: Optional description, max 255 characters.
        created_at: Timestamp when the record was created.
    """

    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
