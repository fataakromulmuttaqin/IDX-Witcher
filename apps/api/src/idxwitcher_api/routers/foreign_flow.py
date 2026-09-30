"""Foreign flow router."""

from fastapi import APIRouter

router = APIRouter(prefix="/foreign-flow", tags=["Foreign Flow"])


@router.get("/{ticker}")
def get_foreign_flow(ticker: str):
    return {
        "ticker": ticker.upper(),
        "status": "ok",
        "message": "Foreign flow data not yet available via public API. Use /ingestion endpoints to populate OHLCV and market data.",
        "data": [],
    }

