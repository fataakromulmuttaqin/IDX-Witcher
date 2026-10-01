"""Database session management."""

from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from idxwitcher_api.core.config import get_settings

settings = get_settings()

# Default to SQLite for local dev if no DATABASE_URL is set.
_default_db = "sqlite:///./idxwitcher_dev.db"

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
