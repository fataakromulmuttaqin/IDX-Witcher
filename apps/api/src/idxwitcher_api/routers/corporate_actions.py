"""Corporate actions router."""

from fastapi import APIRouter

router = APIRouter(prefix="/corporate-actions", tags=["Corporate Actions"])


@router.get("/{ticker}")
def get_corporate_actions(ticker: str):
    return {
        "ticker": ticker.upper(),
        "status": "ok",
        "message": "Corporate actions data not yet available via public API. Coming via IDX integration.",
        "data": [],
    }

