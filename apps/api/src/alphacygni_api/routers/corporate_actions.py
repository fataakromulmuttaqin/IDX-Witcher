"""Corporate actions router (placeholder for IDX integration)."""

from fastapi import APIRouter

router = APIRouter(prefix="/corporate-actions", tags=["Corporate Actions"])


@router.get("/{ticker}")
def get_corporate_actions(ticker: str):
    return {
        "ticker": ticker.upper(),
        "status": "placeholder",
        "message": "Requires IDX corporate actions data integration.",
        "data": [],
    }
