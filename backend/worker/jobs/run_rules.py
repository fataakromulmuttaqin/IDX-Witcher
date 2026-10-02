import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import Signal, WatchlistMember
from core.rules import apply_rule, load_rules
from worker.indicators import add_rule_columns, compute_indicators
from worker.runlog import logged_run


def sector_ranking(df: pd.DataFrame, top: int = 3, min_members: int = 5) -> pd.DataFrame:
    liquid = df[(df["value_avg20"] >= 1e9) & df["sector_id"].notna()]
    g = liquid.groupby("sector_id")
    stats = pd.DataFrame({
        "members": g.size(),
        "med_ret_3m": g["ret_3m"].median(),
        "pct_above_sma50": g.apply(lambda x: (x["close"] > x["sma50"]).mean()),
    })
    stats = stats[stats["members"] >= min_members].copy()
    if stats.empty:
        return stats.assign(score=[], rank=[], is_leading=[])
    stats["score"] = (0.6 * stats["med_ret_3m"].rank(pct=True)
                      + 0.4 * stats["pct_above_sma50"].rank(pct=True))
    stats["rank"] = stats["score"].rank(ascending=False, method="first").astype(int)
    stats["is_leading"] = stats["rank"] <= top
    return stats.sort_values("rank")


def _f(x):
    return None if pd.isna(x) else round(float(x), 4)


def build_signals(today: pd.DataFrame, prev: pd.DataFrame, day) -> list[dict]:
    p = prev.set_index("ticker")[["close", "sma50", "sma200"]].add_prefix("p_")
    d = today.set_index("ticker").join(p, how="left")
    liquid = d["value_avg20"] >= 1e9
    checks = {
        "new_high": d["close"] >= d["hi_52w"],
        "new_low": d["close"] <= d["lo_52w"],
        "volume_surge": (d["volume"] >= 2 * d["vol_avg20"]) & (d["value_traded"] >= 1e9),
        "big_move": (d["ret_1d"].abs() >= 0.07) & liquid,
        "breakdown_sma50": (d["p_close"] >= d["p_sma50"]) & (d["close"] < d["sma50"]),
        "breakout_sma50": (d["p_close"] < d["p_sma50"]) & (d["close"] >= d["sma50"]),
        "breakdown_sma200": (d["p_close"] >= d["p_sma200"]) & (d["close"] < d["sma200"]),
        "breakout_sma200": (d["p_close"] < d["p_sma200"]) & (d["close"] >= d["sma200"]),
    }
    rows = []
    for kind, mask in checks.items():
        for ticker, r in d[mask.fillna(False)].iterrows():
            ratio = r["volume"] / r["vol_avg20"] if r["vol_avg20"] else None
            rows.append({
                "trade_date": day,
                "ticker": ticker,
                "kind": kind,
                "detail": {
                    "close": _f(r["close"]),
                    "ret_1d": _f(r["ret_1d"]),
                    "vol_ratio": _f(ratio) if ratio is not None else None,
                },
            })
    return rows


def run(calendar_days: int = 500) -> dict:
    with logged_run("rules") as res, SessionLocal() as s:
        px = pd.read_sql(
            text("""
                    SELECT p.ticker, p.trade_date AS date, p.high, p.low, p.close, p.volume,
                           p.value_traded, c.sector_id
                    FROM prices_daily p
                    JOIN companies c ON c.ticker = p.ticker
                    WHERE NOT p.is_suspect AND c.is_active
                      AND p.trade_date >= CURRENT_DATE - CAST(:d AS integer)
                """),
            s.connection(),
            params={"d": calendar_days},
        )
        if px.empty:
            return res
        for c in ["high", "low", "close", "volume", "value_traded"]:
            px[c] = px[c].astype(float)
        sector = px.groupby("ticker")["sector_id"].last()
        df = add_rule_columns(compute_indicators(px.drop(columns=["sector_id"])))
        df["sector_id"] = df["ticker"].map(sector)

        days = sorted(df["date"].unique())
        day, prev_day = days[-1], days[-2] if len(days) > 1 else None
        today = df[df["date"] == day].copy()

        rules = {r["slug"]: r for r in load_rules("watchlists")}
        leading = apply_rule(today, rules["leading-stocks"]["expr"])
        today["in_leading_stocks"] = today["ticker"].isin(leading["ticker"])
        ranking = sector_ranking(today)
        sector_ids = ranking.index[ranking["is_leading"]].astype(int).tolist()

        members = []
        for slug, r in rules.items():
            hit = apply_rule(today, r["expr"], leading_sector_ids=sector_ids)
            hit = hit.sort_values("rs_rating", ascending=False, na_position="last")
            members += [
                {"slug": slug, "trade_date": day, "ticker": t, "rank": i + 1}
                for i, t in enumerate(hit["ticker"])
            ]
        res["rows"] += upsert(s, WatchlistMember, members, ["slug", "trade_date", "ticker"])

        if prev_day is not None:
            sigs = build_signals(today, df[df["date"] == prev_day], day)
            res["rows"] += upsert(s, Signal, sigs, ["trade_date", "ticker", "kind"])
        s.commit()
    return res
