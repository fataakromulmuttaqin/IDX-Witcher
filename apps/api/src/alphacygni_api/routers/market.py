"""Market summary router."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from Alpha Cygni_api.db import get_db
from Alpha Cygni_api.db.models import MarketSummary, OHLCV

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/summary")
def market_summary(db: Session = Depends(get_db)):
    latest = (
        db.query(MarketSummary)
        .filter(MarketSummary.index_code == "^JKSE")
        .order_by(MarketSummary.date.desc())
        .first()
    )
    if not latest:
        return {"ihsg": None, "message": "No market summary data available"}

    return {
        "date": latest.date,
        "index_code": latest.index_code,
        "index_name": latest.index_name,
        "open": latest.open_value,
        "high": latest.high_value,
        "low": latest.low_value,
        "close": latest.close_value,
        "change": latest.change,
        "change_percent": latest.change_percent,
        "volume": latest.volume,
        "value": latest.value,
    }


@router.get("/top-movers")
def top_movers(limit: int = 10, db: Session = Depends(get_db)):
    """Return tickers with highest latest close * volume (proxy)."""
    subq = (
        db.query(OHLCV.code, func.max(OHLCV.date).label("max_date"))
        .group_by(OHLCV.code)
        .subquery()
    )
    results = (
        db.query(OHLCV)
        .join(subq, (OHLCV.code == subq.c.code) & (OHLCV.date == subq.c.max_date))
        .order_by(OHLCV.volume.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "code": r.code,
            "date": r.date,
            "close": r.close_price,
            "volume": r.volume,
        }
        for r in results
    ]
