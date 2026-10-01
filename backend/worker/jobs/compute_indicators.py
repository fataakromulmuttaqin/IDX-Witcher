import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import IndicatorDaily
from worker.indicators import compute_indicators
from worker.runlog import logged_run

FLOAT_COLS = ["high", "low", "close", "volume", "value_traded"]
KEEP = ["ticker", "date", "ret_1d", "ret_1m", "ret_3m", "ret_ytd", "ret_1y",
        "sma20", "sma50", "sma150", "sma200", "hi_52w", "lo_52w",
        "vol_avg20", "value_avg20", "atr14", "rs_rating"]


def run(calendar_days: int = 500, write_last_sessions: int = 10) -> dict:
    with logged_run("indicators") as res:
        with SessionLocal() as s:
            df = pd.read_sql(
                text("""
                    SELECT ticker, trade_date AS date, high, low, close, volume, value_traded
                    FROM prices_daily
                    WHERE NOT is_suspect AND trade_date >= CURRENT_DATE - CAST(:d AS integer)
                    ORDER BY ticker, trade_date
                """),
                s.connection(),
                params={"d": calendar_days},
            )
            if df.empty:
                return res
            for c in FLOAT_COLS:
                df[c] = df[c].astype(float)
            ind = compute_indicators(df)
            last_dates = sorted(ind["date"].unique())[-write_last_sessions:]
            out = ind[ind["date"].isin(last_dates)][KEEP].rename(columns={"date": "trade_date"})
            out["rs_rating"] = out["rs_rating"].astype("Int64")
            out = out.astype(object).where(out.notna(), None)
            res["rows"] = upsert(s, IndicatorDaily, out.to_dict("records"), ["ticker", "trade_date"])
            s.commit()
    return res
