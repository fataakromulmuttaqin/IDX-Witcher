"""Screener router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Alpha Cygni_api.db import get_db
from Alpha Cygni_api.db.models import Company, OHLCV

router = APIRouter(prefix="/screen", tags=["Screener"])


@router.get("")
def screen(
    sector: str | None = None,
    min_price: float | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Basic screener by sector and latest close."""
    from sqlalchemy import func

    latest_sub = (
        db.query(OHLCV.code, func.max(OHLCV.date).label("max_date"))
        .group_by(OHLCV.code)
        .subquery()
    )

    query = (
        db.query(Company, OHLCV)
        .join(OHLCV, Company.code == OHLCV.code)
        .join(latest_sub, (OHLCV.code == latest_sub.c.code) & (OHLCV.date == latest_sub.c.max_date))
    )

    if sector:
        query = query.filter(Company.sector.ilike(f"%{sector}%"))

    if min_price is not None:
        query = query.filter(OHLCV.close_price >= min_price)

    results = query.limit(limit).all()

    return [
        {
            "code": company.code,
            "name": company.name,
            "sector": company.sector,
            "close": ohlcv.close_price,
            "volume": ohlcv.volume,
            "date": ohlcv.date,
        }
        for company, ohlcv in results
    ]
