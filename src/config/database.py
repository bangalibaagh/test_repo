"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

from src.config.settings import settings


def _build_engine():
    """Build the SQLAlchemy engine based on the configured DATABASE_URL.

    Returns:
        A SQLAlchemy engine instance configured for the current database URL.
    """
    kwargs = {}
    if settings.DATABASE_URL.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(settings.DATABASE_URL, **kwargs)


_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = _build_engine()
    return _engine


def _get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_get_engine())
    return _SessionLocal


Base = declarative_base()


def get_db() -> Generator:
    """Yield a database session and ensure it is closed after use.

    Yields:
        A SQLAlchemy database session.
    """
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()
