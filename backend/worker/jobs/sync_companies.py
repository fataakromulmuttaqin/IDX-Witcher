from pathlib import Path

import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import Company, Sector

DATA = Path(__file__).resolve().parents[2] / "data"


def _load_sectors() -> pd.DataFrame:
    return pd.read_csv(DATA / "sectors.csv")


def _load_companies() -> pd.DataFrame:
    df = pd.read_csv(DATA / "companies_seed.csv")
    df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()
    df["yahoo_symbol"] = df["ticker"] + ".JK"
    df["is_active"] = True
    if "is_financial" not in df.columns:
        df["is_financial"] = df["sector_code"].eq("FIN")
    return df


def run() -> dict:
    with SessionLocal() as s:
        sectors = _load_sectors()
        upsert(s, Sector, sectors.to_dict("records"), ["id"])
        ids = {code: int(i) for code, i in zip(sectors["code"], sectors["id"])}

        df = _load_companies()
        unknown = set(df["sector_code"].dropna()) - set(ids)
        if unknown:
            raise ValueError(f"Kode sektor tidak dikenal: {sorted(unknown)}")

        df["sector_id"] = df["sector_code"].map(ids)
        df["is_financial"] = df["is_financial"].fillna(df["sector_code"].eq("FIN"))

        rows = df[["ticker", "yahoo_symbol", "name", "is_active", "sector_id", "is_financial"]].to_dict("records")
        upsert(s, Company, rows, ["ticker"])
        s.commit()
    return {"status": "ok", "rows": len(rows)}
