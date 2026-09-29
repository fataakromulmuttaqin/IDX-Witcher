"""Brokers router (placeholder for IDX integration)."""

from fastapi import APIRouter

router = APIRouter(prefix="/brokers", tags=["Brokers"])


@router.get("")
def list_brokers():
    return {
        "status": "placeholder",
        "message": "Requires IDX broker summary data integration.",
        "data": [],
    }
