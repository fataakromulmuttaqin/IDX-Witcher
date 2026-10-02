from datetime import date as Date
from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import text

from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["sectors"])


@cached()
def build_leading_sectors(on: str | None) -> dict:
    with SessionLocal() as s:
        rows = s.execute(text("""
            SELECT ss.trade_date, ss.rank, ss.is_leading, ss.members, ss.med_ret_3m,
                   ss.pct_above_sma50, ss.score, sc.code, sc.name
            FROM sector_scores ss
            JOIN sectors sc ON sc.id = ss.sector_id
            WHERE ss.trade_date = COALESCE(CAST(:d AS date),
                  (SELECT max(trade_date) FROM sector_scores))
            ORDER BY ss.rank
        """), {"d": on}).mappings().all()
    return {"as_of": rows[0]["trade_date"] if rows else on, "data": [dict(r) for r in rows]}


@router.get("/sectors/leading")
def leading_sectors(date: Annotated[Date | None, Query()] = None):
    return build_leading_sectors(on=date.isoformat() if date else None)
