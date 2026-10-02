from fastapi import APIRouter, Query
from sqlalchemy import text

from app.frame import ALL_COLS, load_frame, latest_as_of
from core.cache import cached

router = APIRouter(tags=["market-map"])


@cached()
def build_market_map(period: str) -> dict:
    df = load_frame()
    if df.empty:
        return {"as_of": None, "period": period, "data": []}

    if period == "today":
        col = "ret_1d"
    elif period == "1m":
        col = "ret_1m"
    elif period == "ytd":
        col = "ret_ytd"
    else:  # 1y
        col = "ret_1y"

    df = df.sort_values("market_cap", ascending=False)
    out = []
    for sector, group in df.groupby("sector", sort=False):
        total = group["market_cap"].sum()
        cum_pct = group["market_cap"].cumsum() / total
        small = group[cum_pct > 0.95]
        main = group[cum_pct <= 0.95]
        for _, r in main.iterrows():
            out.append({
                "ticker": r["ticker"],
                "name": r["name"],
                "sector": sector,
                "market_cap": r["market_cap"],
                "change_pct": r[col],
            })
        if not small.empty:
            out.append({
                "ticker": "LAINNYA",
                "name": "Lainnya",
                "sector": sector,
                "market_cap": float(small["market_cap"].sum()),
                "change_pct": float((small["market_cap"] * small[col]).sum() / small["market_cap"].sum()),
            })
    return {"as_of": latest_as_of(df), "period": period, "data": out}


@router.get("/market-map")
def market_map(period: str = Query("today", pattern="^(today|1m|ytd|1y)$")):
    return build_market_map(period=period)
