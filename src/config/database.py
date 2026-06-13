"""Database configuration module.

This module sets up the SQLAlchemy engine, session factory, declarative base,
and a dependency-injection generator for database sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session and ensure it is closed after use.

    Yields:
        Session: A SQLAlchemy database session bound to the configured engine.

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
