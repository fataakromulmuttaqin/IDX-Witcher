from datetime import date as Date

from fastapi import APIRouter, Query
from sqlalchemy import text

from app.errors import ApiError
from app.frame import ALL_COLS, load_frame
from core.cache import cached
from core.db import SessionLocal
from core.rules import apply_rule, load_rules

router = APIRouter(tags=["screens"])
COLS = ["ticker", "name", "sector", "market_cap", "close", "pe_ttm", "pb", "roe",
        "div_yield", "ret_3m", "rs_rating"]


def _hit(df, expr: str):
    return apply_rule(df, " ".join(expr.split()))


@cached()
def build_screens() -> dict:
    df = load_frame()
    out = []
    for r in load_rules("screens"):
        out.append({"slug": r["slug"], "name": r["name"], "description": r["description"],
                    "expr": r["expr"], "members": 0 if df.empty else len(_hit(df, r["expr"]))})
    return {"as_of": None if df.empty else df["trade_date"].iloc[0], "data": out}


@cached()
def build_screen(slug: str) -> dict:
    spec = next((r for r in load_rules("screens") if r["slug"] == slug), None)
    if spec is None:
        raise ApiError(404, "not_found", f"Screen '{slug}' tidak ada")
    info = {k: spec[k] for k in ("slug", "name", "description", "expr")}
    df = load_frame()
    if df.empty:
        return {"as_of": None, "screen": info, "columns": COLS, "count": 0, "data": []}
    hit = _hit(df, spec["expr"]).sort_values("market_cap", ascending=False, na_position="last")
    cols = [*COLS, "na_reason"]
    data = hit[cols].astype(object).where(hit[cols].notna(), None).to_dict("records")
    for row in data:
        row["score"] = None
    return {"as_of": df["trade_date"].iloc[0], "screen": info, "columns": COLS,
            "count": len(data), "data": data}


@router.get("/screens")
def screens():
    return build_screens()


@router.get("/screens/{slug}")
def screen(slug: str):
    return build_screen(slug=slug)
