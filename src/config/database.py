"""Database configuration module.

Sets up the SQLAlchemy engine, session factory, declarative base,
and provides a dependency for database session management.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)
"""SQLAlchemy engine instance configured from application settings."""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Session factory bound to the application engine."""

Base = declarative_base()
"""Declarative base class for SQLAlchemy ORM models."""


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for dependency injection.

    Yields a SQLAlchemy session and ensures it is closed after use,
    even if an exception occurs.

    Yields:
        Session: An active SQLAlchemy database session.

    Example:
        Use as a FastAPI dependency::

            @app.get("/items")
            def read_items(db: Session = Depends(get_db)):
                return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
