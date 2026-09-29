"""Companies router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Alpha Cygni_api.db import get_db
from Alpha Cygni_api.db.models import Company
from Alpha Cygni_api.schemas.company import CompanyOut

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
