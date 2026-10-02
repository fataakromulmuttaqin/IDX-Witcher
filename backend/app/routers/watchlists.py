from datetime import date as Date
from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import text

from app.errors import ApiError
from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["watchlists"])


@cached()
def build_list() -> dict:
    with SessionLocal() as s:
        rows = s.execute(text("""
            SELECT w.slug, w.name, w.description, w.rule_expr,
                   (SELECT count(*) FROM watchlist_members m
                    WHERE m.slug = w.slug
                      AND m.trade_date = (SELECT max(trade_date) FROM watchlist_members)) AS members
            FROM watchlists w
            ORDER BY w.sort_order, w.slug
        """)).mappings().all()
    return {"data": [dict(r) for r in rows]}


@cached()
def build_watchlist(slug: str, on: str | None) -> dict:
    with SessionLocal() as s:
        w = s.execute(text("SELECT slug, name, description, rule_expr FROM watchlists WHERE slug = :s"),
                      {"s": slug}).mappings().first()
        if w is None:
            raise ApiError(404, "not_found", f"Daftar '{slug}' tidak ada")
        rows = s.execute(text("""
            SELECT m.trade_date, m.rank, c.ticker, c.name, sc.name AS sector, p.close,
                   i.ret_1d, i.ret_1m, i.rs_rating, p.close / NULLIF(i.hi_52w, 0) - 1 AS close_vs_high
            FROM watchlist_members m
            JOIN companies c ON c.ticker = m.ticker
            LEFT JOIN sectors sc ON sc.id = c.sector_id
            JOIN prices_daily p ON p.ticker = m.ticker AND p.trade_date = m.trade_date
            LEFT JOIN indicators_daily i ON i.ticker = m.ticker AND i.trade_date = m.trade_date
            WHERE m.slug = :s
              AND m.trade_date = COALESCE(CAST(:d AS date),
                    (SELECT max(trade_date) FROM watchlist_members WHERE slug = :s))
            ORDER BY m.rank
        """), {"s": slug, "d": on}).mappings().all()
    data = [{k: (float(v) if hasattr(v, "is_finite") else v) for k, v in dict(r).items()} for r in rows]
    return {
        "as_of": data[0]["trade_date"] if data else on,
        "watchlist": dict(w),
        "count": len(data),
        "data": data,
    }


@router.get("/watchlists")
def list_watchlists():
    return build_list()


@router.get("/watchlists/{slug}")
def watchlist(slug: str, date: Annotated[Date | None, Query()] = None):
    return build_watchlist(slug=slug, on=date.isoformat() if date else None)
