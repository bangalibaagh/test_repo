"""Device model module.

Defines the SQLAlchemy ORM model for the devices table.
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class Device(Base):
    """SQLAlchemy model representing a device.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Human-readable name of the device.
        serial_number: Optional unique serial number.
        device_type_id: Foreign key referencing device_types.id.
        location_id: Optional foreign key referencing locations.id.
        device_type: Relationship to DeviceType.
        location: Relationship to Location.
    """

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    device_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("device_types.id"), nullable=False
    )
    location_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=True
    )

    device_type: Mapped["DeviceType"] = relationship(  # noqa: F821
        "DeviceType", lazy="joined"
    )
    location: Mapped["Location | None"] = relationship(  # noqa: F821
        "Location", lazy="joined"
    )
