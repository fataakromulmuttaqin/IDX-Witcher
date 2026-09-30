"""Prices router."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from IDX Witcher_api.db import get_db
from IDX Witcher_api.db.models import OHLCV
from IDX Witcher_api.schemas.ohlcv import OHLCVOut

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/{ticker}", response_model=list[OHLCVOut])
def get_prices(
    ticker: str,
    start: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = 500,
    db: Session = Depends(get_db),
):
    query = db.query(OHLCV).filter(OHLCV.code == ticker.upper())
    if start:
        query = query.filter(OHLCV.date >= start)
    if end:
        query = query.filter(OHLCV.date <= end)
    return query.order_by(OHLCV.date.desc()).limit(limit).all()


@router.get("/{ticker}/latest", response_model=OHLCVOut)
def get_latest_price(ticker: str, db: Session = Depends(get_db)):
    record = (
        db.query(OHLCV)
        .filter(OHLCV.code == ticker.upper())
        .order_by(OHLCV.date.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Price not found")
    return record


@router.get("/{ticker}/range", response_model=list[OHLCVOut])
def get_price_range(ticker: str, days: int = 30, db: Session = Depends(get_db)):
    from datetime import timedelta

    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    return (
        db.query(OHLCV)
        .filter(OHLCV.code == ticker.upper(), OHLCV.date >= start_date, OHLCV.date <= end_date)
        .order_by(OHLCV.date.asc())
        .all()
    )
