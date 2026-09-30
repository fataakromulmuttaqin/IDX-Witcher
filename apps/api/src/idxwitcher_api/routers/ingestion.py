"""Ingestion router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from idxwitcher_api.db import get_db
from idxwitcher_api.services.ingestion import IngestionService
from idxwitcher_api.services.tv_sync import sync_companies_from_tradingview, enrich_company_from_tradingview

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.post("/seed-companies")
def seed_companies(db: Session = Depends(get_db)):
    service = IngestionService(db)
    count = service.seed_companies()
    return {"status": "ok", "seeded": count}


@router.post("/sync-tradingview")
def sync_tradingview(min_market_cap: float | None = None, db: Session = Depends(get_db)):
    """Sync all IDX companies from TradingView scanner into database."""
    result = sync_companies_from_tradingview(db, min_market_cap=min_market_cap)
    return {"status": "ok", "source": "tradingview", **result}


@router.post("/enrich-tradingview/{ticker}")
def enrich_tradingview(ticker: str, db: Session = Depends(get_db)):
    """Enrich single company data from TradingView scanner."""
    data = enrich_company_from_tradingview(db, ticker)
    if not data:
        raise HTTPException(status_code=404, detail="Company not found or no TradingView data")
    return {"status": "ok", "ticker": ticker, "data": data}


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
