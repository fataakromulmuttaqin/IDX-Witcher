"""Health check router."""

from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check() -> dict:
    """Return API health status."""
    return {
        "status": "ok",
        "service": "IDX Witcher-api",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
