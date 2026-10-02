from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import text

from app.errors import ApiError
from core.db import SessionLocal

router = APIRouter(tags=["portfolio"])


class QuoteIn(BaseModel):
    tickers: list[str] = Field(min_length=1, max_length=100)


@router.post("/portfolio/quote")
def quote(body: QuoteIn):
    if not body.tickers:
        raise ApiError(422, "bad_request", "tickers wajib diisi")
    with SessionLocal() as s:
        rows = s.execute(text("""
            SELECT c.ticker, c.name, sc.name AS sector, p.close, p.trade_date
            FROM companies c
            LEFT JOIN sectors sc ON sc.id = c.sector_id
            JOIN LATERAL (SELECT * FROM prices_daily WHERE ticker = c.ticker
                          ORDER BY trade_date DESC LIMIT 1) p ON TRUE
            WHERE c.ticker = ANY(:tickers)
        """), {"tickers": [t.upper() for t in body.tickers]}).mappings().all()
    return {"data": [dict(r) for r in rows]}
