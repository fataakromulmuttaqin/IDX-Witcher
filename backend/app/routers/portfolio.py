from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(tags=["portfolio"])


class QuoteIn(BaseModel):
    tickers: list[str] = Field(min_length=1, max_length=100)


@router.post("/portfolio/quote")
def quote(body: QuoteIn):
    return {"data": []}
