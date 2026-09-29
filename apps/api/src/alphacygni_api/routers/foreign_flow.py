"""Foreign flow router (placeholder for IDX integration)."""

from fastapi import APIRouter

router = APIRouter(prefix="/foreign-flow", tags=["Foreign Flow"])


@router.get("/{ticker}")
def get_foreign_flow(ticker: str):
    return {
        "ticker": ticker.upper(),
        "status": "placeholder",
        "message": "Requires IDX broker/summary data integration. Use /ingestion/ohlcv/{ticker} for Yahoo OHLCV first.",
        "data": [],
    }
