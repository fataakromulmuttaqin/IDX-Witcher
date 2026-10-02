import pandas as pd
from fastapi import APIRouter, Query

from app.errors import ApiError
from app.frame import load_frame
from core.cache import cached
from core.rules import load_rules

router = APIRouter(tags=["screener"])


def add_score(df: pd.DataFrame, higher: list[str], lower: list[str]) -> pd.Series:
    parts = [df[c].rank(pct=True) for c in higher] + [df[c].rank(pct=True, ascending=False) for c in lower]
    if not parts:
        return pd.Series(index=df.index, dtype=float)
    table = pd.concat(parts, axis=1)
    score = table.mean(axis=1) * 100
    return score.where(table.notna().sum(axis=1) >= 3)


@cached()
def build_screener(menu: str, sector: str | None, min_mcap: float, min_value: float,
                   q: str | None, limit: int) -> dict:
    menus = load_rules("menus")
    if not isinstance(menus, dict):
        raise ApiError(500, "internal_error", "Menus config invalid")
    if menu not in menus:
        raise ApiError(404, "not_found", f"Menu '{menu}' tidak ada")
    spec = menus[menu]
    df = load_frame()
    if df.empty:
        return {"as_of": None, "menu": menu, "columns": [*spec["columns"], "score"], "data": []}
    as_of = df["trade_date"].iloc[0]
    needed = {*spec["columns"], *spec["higher"], *spec["lower"], "value_avg20", "market_cap"}
    for col in needed - set(df.columns):
        df[col] = float("nan")
    df["score"] = add_score(df, spec["higher"], spec["lower"])
    if sector:
        df = df[df["sector"] == sector]
    df = df[
        (df["market_cap"].astype(float).fillna(0) >= min_mcap)
        & (df["value_avg20"].astype(float).fillna(0) >= min_value)
    ]
    if q:
        needle = q.lower()
        df = df[
            df["ticker"].str.lower().str.contains(needle)
            | df["name"].str.lower().str.contains(needle)
        ]
    key = "score" if df["score"].notna().any() else "market_cap"
    df = df.sort_values(key, ascending=False, na_position="last")
    if limit > 0:
        df = df.head(limit)
    cols = [*spec["columns"], "score", "na_reason"]
    data = df[cols].astype(object).where(df[cols].notna(), None).to_dict("records")
    return {"as_of": as_of, "menu": menu, "columns": [*spec["columns"], "score"], "data": data}


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
