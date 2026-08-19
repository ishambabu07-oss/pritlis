"""PostgreSQL connection and session management."""

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/space_debris",
)

_engine: Engine | None = None
SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def initialize_database() -> None:
    """Create the application tables if they have not already been migrated."""
    # Importing registers all ORM mappings before metadata is created.
    from app.models.conjunction import Conjunction  # noqa: F401

    Base.metadata.create_all(bind=get_engine())


def get_engine() -> Engine:
    """Create and bind the PostgreSQL engine only when the API starts."""
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        SessionLocal.configure(bind=_engine)
    return _engine
