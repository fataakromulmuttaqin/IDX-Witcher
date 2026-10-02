from fastapi import APIRouter, Query
from sqlalchemy import text

from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["market-map"])
PERIOD_COL = {"today": "ret_1d", "1m": "ret_1m", "ytd": "ret_ytd", "1y": "ret_1y"}


@cached()
def build_market_map(period: str) -> dict:
    col = PERIOD_COL[period]
    sql = text(f"""
        SELECT c.ticker, c.name, s.name AS sector,
               p.close * c.shares_outstanding AS market_cap,
               i.{col} AS change_pct, i.trade_date
        FROM indicators_daily i
        JOIN prices_daily p ON p.ticker = i.ticker AND p.trade_date = i.trade_date
        JOIN companies c ON c.ticker = i.ticker
        LEFT JOIN sectors s ON s.id = c.sector_id
        WHERE i.trade_date = (SELECT max(trade_date) FROM indicators_daily)
          AND c.is_active AND c.shares_outstanding IS NOT NULL
    """)
    with SessionLocal() as s:
        rows = s.execute(sql).mappings().all()
    data = [
        {
            "ticker": r["ticker"],
            "name": r["name"],
            "sector": r["sector"],
            "market_cap": float(r["market_cap"]),
            "change_pct": None if r["change_pct"] is None else float(r["change_pct"]),
        }
        for r in rows
    ]
    return {"as_of": rows[0]["trade_date"] if rows else None, "period": period, "data": data}


@router.get("/market-map")
def market_map(period: str = Query("today", pattern="^(today|1m|ytd|1y)$")):
    return build_market_map(period=period)
