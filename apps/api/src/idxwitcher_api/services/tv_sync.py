"""Syncs TradingView scanner data into local database.

Populates / updates Company table and returns summary statistics.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from idxwitcher_api.db.models import Company
from idxwitcher_api.services.tradingview import TradingViewClient


def sync_companies_from_tradingview(db: Session, min_market_cap: float | None = None) -> dict[str, Any]:
    """Fetch all IDX stocks from TradingView and upsert into companies table."""
    client = TradingViewClient()
    rows = client.scan_all_stocks(min_market_cap=min_market_cap)

    created = 0
    updated = 0
    existing = {c.code for c in db.query(Company.code).all()}

    for row in rows:
        code = row.get("ticker")
        name = row.get("description") or code
        sector = row.get("sector")

        if code in existing:
            company = db.query(Company).filter(Company.code == code).first()
            company.name = name
            company.sector = sector
            company.is_active = True
            company.source = "tradingview"
            updated += 1
        else:
            company = Company(
                code=code,
                name=name,
                sector=sector,
                is_active=True,
                source="tradingview",
            )
            db.add(company)
            created += 1

    db.commit()

    return {
        "total_synced": len(rows),
        "created": created,
        "updated": updated,
    }


def enrich_company_from_tradingview(db: Session, code: str) -> dict[str, Any] | None:
    """Fetch single ticker from TradingView and update company record."""
    client = TradingViewClient()
    data = client.quote(code)
    if not data:
        return None

    company = db.query(Company).filter(Company.code == code.upper().replace(".JK", "")).first()
    if not company:
        return None

    company.name = data.get("description") or company.name
    company.sector = data.get("sector") or company.sector
    company.is_active = True
    company.source = "tradingview"
    db.commit()

    return data
