from fastapi import APIRouter

router = APIRouter(tags=["stocks"])


@router.get("/stocks/{ticker}")
def stock(ticker: str):
    return {"ticker": ticker}
