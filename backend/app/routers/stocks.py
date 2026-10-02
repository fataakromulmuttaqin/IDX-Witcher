from fastapi import APIRouter, Query
from sqlalchemy import text

from app.errors import ApiError
from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["stocks"])
RANGE_DAYS = {"1m": 31, "3m": 93, "1y": 366, "5y": 1830, "max": 36500}

SQL_STOCK = text("""
    SELECT c.ticker, c.name, s.name AS sector, p.close, p.trade_date,
           to_jsonb(i) - 'ticker' - 'trade_date' AS ind,
           to_jsonb(f) - 'ticker' - 'as_of' AS fun
    FROM companies c
    LEFT JOIN sectors s ON s.id = c.sector_id
    JOIN LATERAL (SELECT * FROM prices_daily WHERE ticker = c.ticker
                  ORDER BY trade_date DESC LIMIT 1) p ON TRUE
    LEFT JOIN indicators_daily i ON i.ticker = c.ticker AND i.trade_date = p.trade_date
    LEFT JOIN LATERAL (SELECT * FROM fundamentals_snapshot x WHERE x.ticker = c.ticker
                       ORDER BY as_of DESC LIMIT 1) f ON TRUE
    WHERE c.ticker = :t
""")


@cached()
def build_stock(ticker: str) -> dict:
    with SessionLocal() as s:
        r = s.execute(SQL_STOCK, {"t": ticker}).mappings().first()
        if r is None:
            raise ApiError(404, "not_found", f"Ticker {ticker} tidak ditemukan")
        sigs = s.execute(text("""
            SELECT trade_date, kind, detail FROM signals
            WHERE ticker = :t ORDER BY trade_date DESC, kind LIMIT 20
        """), {"t": ticker}).mappings().all()
    fun = dict(r["fun"] or {})
    na = fun.pop("na_reason", {}) or {}
    return {
        "as_of": r["trade_date"],
        "ticker": r["ticker"],
        "name": r["name"],
        "sector": r["sector"],
        "close": float(r["close"]),
        "indicators": r["ind"] or {},
        "fundamentals": fun,
        "na_reason": na,
        "signals": [dict(x) for x in sigs],
    }


@cached()
def build_prices(ticker: str, range_: str) -> dict:
    with SessionLocal() as s:
        rows = s.execute(text("""
            SELECT trade_date AS time, open, high, low, close, volume FROM prices_daily
            WHERE ticker = :t AND NOT is_suspect
              AND trade_date >= CURRENT_DATE - CAST(:d AS integer)
            ORDER BY trade_date
        """), {"t": ticker, "d": RANGE_DAYS[range_]}).mappings().all()
    return {
        "ticker": ticker,
        "range": range_,
        "data": [{k: (float(v) if hasattr(v, "is_finite") else v) for k, v in dict(r).items()} for r in rows],
    }


@router.get("/stocks/{ticker}")
def stock(ticker: str):
    return build_stock(ticker=ticker.upper())


@router.get("/stocks/{ticker}/prices")
def prices(ticker: str, range: str = Query("1y", pattern="^(1m|3m|1y|5y|max)$")):
    return build_prices(ticker=ticker.upper(), range_=range)
