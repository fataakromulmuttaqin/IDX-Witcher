from fastapi import APIRouter, Query

router = APIRouter(tags=["screener"])


@router.get("/screener")
def screener(
    menu: str = "valuation",
    sector: str | None = None,
    min_mcap: float = Query(0, ge=0),
    min_value: float = Query(0, ge=0),
    q: str | None = Query(None, max_length=50),
    limit: int = Query(0, ge=0, le=1000),
):
    return {"as_of": None, "menu": menu, "columns": [], "data": []}
