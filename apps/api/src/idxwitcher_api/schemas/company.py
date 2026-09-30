"""Company schemas."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class CompanyOut(BaseModel):
    code: str
    name: str
    sector: str | None = None
    sub_sector: str | None = None
    listing_date: date | None = None
    is_active: bool
    source: str

    model_config = ConfigDict(from_attributes=True)
