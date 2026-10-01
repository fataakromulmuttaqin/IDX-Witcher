from fastapi import APIRouter, Query

router = APIRouter(tags=["feed"])


@router.get("/feed")
def feed(days: int = Query(5, ge=1, le=20), kind: str | None = None, sector: str | None = None):
    return {"days": days, "data": []}
