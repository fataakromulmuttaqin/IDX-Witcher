from fastapi import APIRouter

from idxwitcher_api.db import get_db

router = APIRouter(prefix="/brokers", tags=["Brokers"])


@router.get("")
def list_brokers():
    return {
        "status": "ok",
        "message": "Broker summary data not yet available via public API. Use /market/summary and /prices for market data.",
        "data": [],
    }

