"""Device type ORM model.

Defines the SQLAlchemy model for the device_types table.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class DeviceType(Base):
    """SQLAlchemy model representing a device type.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Unique, non-nullable name of the device type.
        description: Optional description of the device type.
    """

    __tablename__ = "device_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
