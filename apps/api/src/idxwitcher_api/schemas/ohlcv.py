"""OHLCV schemas."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OHLCVOut(BaseModel):
    code: str
    date: date
    open_price: Decimal | None = None
    high_price: Decimal | None = None
    low_price: Decimal | None = None
    close_price: Decimal | None = None
    volume: int | None = None
    value: Decimal | None = None
    frequency: int | None = None
    source: str

    model_config = ConfigDict(from_attributes=True)
