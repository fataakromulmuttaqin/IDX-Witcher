from fastapi import APIRouter, Query

from app.errors import ApiError
from app.frame import ALL_COLS, load_frame, latest_as_of
from core.cache import cached
from core.rules import load_rules

router = APIRouter(tags=["screener"])

# Kolom dasar untuk setiap menu screener
MENU_BASE = ["ticker", "name", "sector", "market_cap", "close"]


def _score(df, higher, lower):
    """Hitung skor persentil rata-rata dari kolom higher (lebih tinggi lebih baik)
    dan lower (lebih rendah lebih baik, dibalik).
    """
    import pandas as pd
    metrics = [c for c in (higher + lower) if c in df.columns]
    if not metrics or len(df) == 0:
        return pd.Series(index=df.index, dtype="float64")
    pct = pd.DataFrame(index=df.index)
    for c in metrics:
        s = pd.to_numeric(df[c], errors="coerce")
        if c in higher:
            pct[c] = s.rank(pct=True)
        else:
            pct[c] = (s * -1).rank(pct=True)
    return pct.mean(axis=1) * 100


@cached()
def build_screener(menu: str, sector: str | None, min_mcap: float, min_value: float,
                   q: str | None, limit: int) -> dict:
    menus = load_rules("menus")
    if menu not in menus:
        raise ApiError(404, "not_found", f"Menu '{menu}' tidak ada")
    spec = menus[menu]
    cols = [*MENU_BASE, *spec["columns"], "score", "na_reason"]

    df = load_frame()
    if df.empty:
        return {"as_of": None, "menu": menu, "columns": cols, "data": []}

    if sector:
        df = df[df["sector"] == sector]
    if min_mcap:
        df = df[df["market_cap"] >= min_mcap]
    if min_value:
        df = df[df["value_avg20"] >= min_value]
    if q:
        q = q.upper()
        df = df[df["ticker"].str.contains(q, na=False) | df["name"].str.contains(q, na=False)]

    df["score"] = _score(df, spec.get("higher", []), spec.get("lower", []))

    if not spec.get("higher") and not spec.get("lower"):
        df = df.sort_values("market_cap", ascending=False, na_position="last")
    else:
        df = df.sort_values("score", ascending=False, na_position="last")

    if limit > 0:
        df = df.head(limit)

    for c in ALL_COLS:
        if c not in df.columns:
            df[c] = float("nan")
    out_cols = [c for c in cols if c in df.columns]
    data = df[out_cols].astype(object).where(df[out_cols].notna(), None).to_dict("records")
    return {"as_of": latest_as_of(df), "menu": menu, "columns": out_cols, "data": data}


@router.get("/screener")
def screener(
    menu: str = "valuation",
    sector: str | None = None,
    min_mcap: float = Query(0, ge=0),
    min_value: float = Query(0, ge=0),
    q: str | None = Query(None, max_length=50),
    limit: int = Query(0, ge=0, le=1000),
):
    return build_screener(menu=menu, sector=sector, min_mcap=min_mcap,
                         min_value=min_value, q=q, limit=limit)
