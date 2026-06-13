"""Location model module.

Defines the SQLAlchemy ORM model for the locations resource.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class Location(Base):
    """SQLAlchemy model representing a location.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Unique, non-nullable name of the location.
        address: Optional address string.
        description: Optional description string.
    """

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
