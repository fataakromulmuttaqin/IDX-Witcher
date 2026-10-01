"""Database session management."""

from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from idxwitcher_api.core.config import get_settings

import os

settings = get_settings()

# Default to SQLite for local dev if no DATABASE_URL is set.
# Use absolute path so the DB file is stable regardless of cwd.
_default_db_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "idxwitcher_dev.db")
)
_default_db = f"sqlite:///{_default_db_path}"

DATABASE_URL = settings.database_url or _default_db

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
