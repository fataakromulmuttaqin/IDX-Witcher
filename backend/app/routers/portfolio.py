from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import text

from core.db import SessionLocal

router = APIRouter(tags=["portfolio"])


class QuoteIn(BaseModel):
    tickers: list[str] = Field(min_length=1, max_length=100)


@router.post("/portfolio/quote")
def quote(body: QuoteIn):
    tickers = sorted({t.strip().upper() for t in body.tickers})
    sql = text("""
        SELECT DISTINCT ON (p.ticker) p.ticker, p.close, p.trade_date, s.name AS sector
        FROM prices_daily p
        JOIN companies c ON c.ticker = p.ticker
        LEFT JOIN sectors s ON s.id = c.sector_id
        WHERE p.ticker = ANY(:t)
        ORDER BY p.ticker, p.trade_date DESC
    """)
    with SessionLocal() as s:
        rows = s.execute(sql, {"t": tickers}).mappings().all()
    return {"data": [
        {"ticker": r["ticker"], "close": float(r["close"]),
         "trade_date": r["trade_date"], "sector": r["sector"]}
        for r in rows
    ]}
