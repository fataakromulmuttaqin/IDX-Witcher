from fastapi import APIRouter, Query

router = APIRouter(tags=["market-map"])


@router.get("/market-map")
def market_map(period: str = Query("today", pattern="^(today|1m|ytd|1y)$")):
    return {"as_of": None, "period": period, "data": []}
