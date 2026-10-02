import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal

ALL_COLS = [
    "close", "market_cap", "ret_1d", "ret_1m", "ret_3m", "ret_ytd", "ret_1y", "sma20", "sma50",
    "sma150", "sma200", "hi_52w", "lo_52w", "vol_avg20", "value_avg20", "atr14", "rs_rating",
    "pe_ttm", "pb", "ps", "ev_ebitda", "roe", "roa", "gross_margin", "op_margin", "net_margin",
    "debt_equity", "current_ratio", "div_yield", "payout", "revenue_ttm", "net_income_ttm",
    "fcf_ttm", "rev_growth_yoy", "eps_growth_yoy",
]

TEXT_COLS = ["ticker", "name", "sector"]

SQL = text("""
    SELECT c.ticker, c.name, s.code AS sector, p.close, p.trade_date,
           p.close * c.shares_outstanding AS market_cap,
           to_jsonb(i) - 'ticker' - 'trade_date' AS ind,
           to_jsonb(f) - 'ticker' - 'as_of' AS fun
    FROM companies c
    JOIN prices_daily p ON p.ticker = c.ticker
         AND p.trade_date = (SELECT max(trade_date) FROM indicators_daily)
    LEFT JOIN indicators_daily i ON i.ticker = c.ticker AND i.trade_date = p.trade_date
    LEFT JOIN LATERAL (SELECT * FROM fundamentals_snapshot x WHERE x.ticker = c.ticker
                       ORDER BY as_of DESC LIMIT 1) f ON TRUE
    LEFT JOIN sectors s ON s.id = c.sector_id
    WHERE c.is_active
""")


def _num(v):
    """Konversi Decimal/None ke float agar aman untuk pandas."""
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_frame() -> pd.DataFrame:
    """Satu baris per saham aktif pada tanggal data terbaru: harga, indikator, fundamental."""
    with SessionLocal() as s:
        raw = s.execute(SQL).mappings().all()
    records = []
    for r in raw:
        row = {k: _num(v) if k != "sector" else v for k, v in dict(r).items()
               if k not in ("ind", "fun")}
        mcap = row.get("market_cap")
        row.update(r["ind"] or {})
        fun = dict(r["fun"] or {})
        row["na_reason"] = fun.pop("na_reason", {}) or {}
        row.update({k: _num(v) for k, v in fun.items()})
        # market cap selalu dari harga terbaru, bukan snapshot mingguan
        row["market_cap"] = mcap
        records.append(row)
    df = pd.DataFrame(records)
    if df.empty:
        return df
    for c in ALL_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df.columns else float("nan")
    for c in TEXT_COLS:
        if c not in df.columns:
            df[c] = None
    return df


def latest_as_of(df: pd.DataFrame) -> str | None:
    if df.empty or "trade_date" not in df.columns:
        return None
    v = df["trade_date"].iloc[0]
    return v.isoformat() if hasattr(v, "isoformat") else str(v)
