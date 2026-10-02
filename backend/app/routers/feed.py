from fastapi import APIRouter, Query
from sqlalchemy import text

from app.frame import load_frame, latest_as_of
from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["feed"])


@cached()
def build_feed(days: int, kind: str | None, sector: str | None) -> dict:
    with SessionLocal() as s:
        sql = """
            SELECT s.trade_date, s.ticker, c.name, sec.name AS sector,
                   s.kind, s.detail
            FROM signals s
            JOIN companies c ON c.ticker = s.ticker
            LEFT JOIN sectors sec ON sec.id = c.sector_id
            WHERE s.trade_date >= CURRENT_DATE - CAST(:days AS integer)
        """
        params = {"days": days}
        if kind:
            sql += " AND s.kind = :kind"
            params["kind"] = kind
        if sector:
            sql += " AND sec.name = :sector"
            params["sector"] = sector
        sql += " ORDER BY s.trade_date DESC, s.ticker, s.kind"
        rows = s.execute(text(sql), params).mappings().all()
    return {"days": days, "as_of": latest_as_of(load_frame()), "data": [dict(r) for r in rows]}


@router.get("/feed")
def feed(days: int = Query(5, ge=1, le=20), kind: str | None = None, sector: str | None = None):
    return build_feed(days=days, kind=kind, sector=sector)
