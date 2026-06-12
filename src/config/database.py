"""Database configuration and session management."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.config.settings import settings

_connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def _get_session_local() -> sessionmaker:
    """Return the current SessionLocal factory.

    Returns:
        The SQLAlchemy sessionmaker instance used to create database sessions.
    """
    return SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use.

    Yields:
        A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
