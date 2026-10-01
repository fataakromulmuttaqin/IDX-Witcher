from fastapi import APIRouter
from sqlalchemy import text

from core.db import SessionLocal

router = APIRouter(tags=["meta"])


@router.get("/health")
def health():
    with SessionLocal() as s:
        s.execute(text("SELECT 1"))
    return {"status": "ok"}


@router.get("/meta")
def meta():
    with SessionLocal() as s:
        as_of = s.execute(text("SELECT max(trade_date) FROM indicators_daily")).scalar()
        n = s.execute(text("SELECT count(*) FROM companies WHERE is_active")).scalar()
        run = s.execute(
            text(
                "SELECT job, status, finished_at FROM ingest_runs ORDER BY id DESC LIMIT 1"
            )
        ).mappings().first()
    return {"as_of": as_of, "active_companies": n, "last_run": dict(run) if run else None}
