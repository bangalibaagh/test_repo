"""Database configuration module for the Device Registry application.

This module sets up the SQLAlchemy engine, session factory, declarative
base, and a dependency-injection-compatible session generator.
"""

from typing import Generator

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
"""Declarative base class for all SQLAlchemy ORM models."""


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy database session and ensure it is closed afterward.

    This generator is intended for use as a FastAPI dependency. It creates
    a new ``SessionLocal`` session, yields it to the caller, and guarantees
    the session is closed in a ``finally`` block regardless of whether an
    exception occurred.

    Yields:
        Session: An active SQLAlchemy ORM session.

    Example::

        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
