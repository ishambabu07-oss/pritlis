"""PostgreSQL connection and session management."""

import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg:///space_debris",
)

_engine: Engine | None = None
SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def initialize_database() -> None:
    """Migrate the legacy empty table and create the application schema."""
    # Importing registers all ORM mappings before metadata is created.
    from app.models.conjunction import Conjunction  # noqa: F401

    engine = get_engine()
    _migrate_empty_legacy_conjunctions(engine)
    Base.metadata.create_all(bind=engine)


def _migrate_empty_legacy_conjunctions(engine: Engine) -> None:
    """Replace the original two-column placeholder table when it contains no data.

    A populated legacy table lacks the fields needed to construct a valid
    conjunction alert, so it is intentionally left untouched and startup fails
    with an actionable migration error instead of silently discarding data.
    """
    inspector = inspect(engine)
    if "conjunctions" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("conjunctions")}
    if columns != {"id", "created_at"}:
        return

    with engine.begin() as connection:
        row_count = connection.execute(text("SELECT count(*) FROM conjunctions")).scalar_one()
        if row_count:
            raise RuntimeError(
                "The legacy conjunctions table contains data and requires a manual migration."
            )
        connection.execute(text("DROP TABLE conjunctions"))


def get_engine() -> Engine:
    """Create and bind the PostgreSQL engine only when the API starts."""
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        SessionLocal.configure(bind=_engine)
    return _engine
