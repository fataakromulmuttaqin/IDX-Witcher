from fastapi import APIRouter, Query
from sqlalchemy import text

from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["feed"])


@cached(ttl=3600)
def build_feed(days: int, kind: str | None, sector: str | None) -> dict:
    sql = text("""
        SELECT sg.trade_date, sg.ticker, c.name, s.code AS sector, sg.kind, sg.detail
        FROM signals sg
        JOIN companies c ON c.ticker = sg.ticker
        LEFT JOIN sectors s ON s.id = c.sector_id
        WHERE sg.trade_date IN (SELECT DISTINCT trade_date FROM signals
                                ORDER BY trade_date DESC LIMIT :days)
          AND (CAST(:kind AS text) IS NULL OR sg.kind = CAST(:kind AS text))
          AND (CAST(:sector AS text) IS NULL OR s.code = CAST(:sector AS text))
        ORDER BY sg.trade_date DESC, sg.ticker
    """)
    with SessionLocal() as s:
        rows = s.execute(sql, {"days": days, "kind": kind, "sector": sector}).mappings().all()
    return {"days": days, "data": [dict(r) for r in rows]}


@router.get("/feed")
def feed(days: int = Query(5, ge=1, le=20), kind: str | None = None, sector: str | None = None):
    return build_feed(days=days, kind=kind, sector=sector)
