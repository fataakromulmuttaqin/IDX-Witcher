"""Companies router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from idxwitcher_api.db import get_db
from idxwitcher_api.db.models import Company
from idxwitcher_api.schemas.company import CompanyOut
from idxwitcher_api.services.investing import InvestingClient
from idxwitcher_api.services.idx_client import IDXDataClient

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("", response_model=list[CompanyOut])
def list_companies(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    return db.query(Company).offset(offset).limit(limit).all()


@router.get("/{code}", response_model=CompanyOut)
def get_company(code: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.code == code.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/{code}/details")
def get_company_details(code: str, db: Session = Depends(get_db)):
    """Return company details enriched with Investing.com and IDX fallback data."""
    company = db.query(Company).filter(Company.code == code.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    investing_client = InvestingClient()
    idx_client = IDXDataClient()

    investing_data = investing_client.fetch_quote(code)
    idx_details = idx_client.fetch_company_details(code)
    idx_quote = idx_client.fetch_latest_quote(code)

    return {
        "code": company.code,
        "name": company.name,
        "sector": company.sector,
        "source": company.source,
        "investing": investing_data,
        "idx": {
            "profile": idx_details,
            "quote": idx_quote,
        },
    }
