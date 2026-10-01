from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=10)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def upsert(session, model, rows: list[dict], keys: list[str], chunk: int = 2000) -> int:
    if not rows:
        return 0
    cols = [c for c in rows[0].keys() if c not in keys]
    for i in range(0, len(rows), chunk):
        stmt = insert(model).values(rows[i : i + chunk])
        stmt = stmt.on_conflict_do_update(
            index_elements=keys, set_={c: stmt.excluded[c] for c in cols}
        )
        session.execute(stmt)
    return len(rows)
