"""Ingestion router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from IDX Witcher_api.db import get_db
from IDX Witcher_api.services.ingestion import IngestionService

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.post("/seed-companies")
def seed_companies(db: Session = Depends(get_db)):
    service = IngestionService(db)
    count = service.seed_companies()
    return {"status": "ok", "seeded": count}


@router.post("/ohlcv/{ticker}")
def ingest_ohlcv(ticker: str, period: str = "1y", db: Session = Depends(get_db)):
    service = IngestionService(db)
    rows = service.ingest_ohlcv_yahoo(ticker, period=period)
    return {"status": "ok", "ticker": ticker, "rows_inserted": rows}


@router.post("/batch")
def ingest_batch(tickers: str, period: str = "1y", db: Session = Depends(get_db)):
    codes = [c.strip().upper() for c in tickers.split(",")]
    service = IngestionService(db)
    results = service.ingest_ohlcv_batch(codes, period=period)
    return {"status": "ok", "results": results}


@router.post("/market-summary")
def ingest_market(index_code: str = "^JKSE", period: str = "1y", db: Session = Depends(get_db)):
    service = IngestionService(db)
    rows = service.ingest_market_summary(index_code=index_code, period=period)
    return {"status": "ok", "index_code": index_code, "rows_inserted": rows}
