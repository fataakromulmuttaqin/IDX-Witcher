import math

import pandas as pd

FIN_NA = {"debt_equity", "current_ratio", "ev_ebitda", "gross_margin"}   # tidak berlaku bagi bank dll.
LOSS_COLS = {"pe_ttm", "payout"}                                          # kosong karena laba negatif
LIMITS = {"pe_ttm": (0, 1000), "pb": (0, 100), "roe": (-5, 5)}            # di luar rentang = n/a


def _row(df: pd.DataFrame | None, items: tuple[str, ...]) -> pd.Series | None:
    """df kuartalan yfinance: baris = item, kolom = tanggal. Urut dari terbaru."""
    if df is None or df.empty:
        return None
    for it in items:
        if it in df.index:
            s = pd.to_numeric(df.loc[it], errors="coerce").dropna()
            if len(s):
                return s.sort_index(ascending=False)
    return None


def ttm(df, *items):
    s = _row(df, items)
    return float(s.iloc[:4].sum()) if s is not None and len(s) >= 4 else None


def latest(df, *items):
    s = _row(df, items)
    return float(s.iloc[0]) if s is not None else None


def yoy(df, *items):
    """Kuartal terakhir dibanding kuartal sama tahun lalu (butuh 5 kuartal, basis > 0)."""
    s = _row(df, items)
    if s is None or len(s) < 5 or s.iloc[4] <= 0:
        return None
    return float(s.iloc[0] / s.iloc[4] - 1)


def _div(a, b):
    return a / b if a is not None and b is not None and b > 0 else None


def compute_snapshot(*, price, shares, is_financial, info, income, balance, cashflow,
                     fx=None, div12=0.0) -> dict:
    k = fx if (info.get("financialCurrency") == "USD" and fx) else 1.0
    scale = lambda v: None if v is None else v * k   # noqa: E731

    rev = scale(ttm(income, "Total Revenue", "Operating Revenue"))
    ni = scale(ttm(income, "Net Income", "Net Income Common Stockholders"))
    gp = scale(ttm(income, "Gross Profit"))
    oi = scale(ttm(income, "Operating Income"))
    ebitda = scale(ttm(income, "EBITDA", "Normalized EBITDA"))
    fcf = scale(ttm(cashflow, "Free Cash Flow"))
    equity = scale(latest(balance, "Stockholders Equity", "Common Stock Equity"))
    assets = scale(latest(balance, "Total Assets"))
    debt = scale(latest(balance, "Total Debt"))
    cash = scale(latest(balance, "Cash And Cash Equivalents"))
    cur_a = latest(balance, "Current Assets")
    cur_l = latest(balance, "Current Liabilities")

    mcap = price * shares if price and shares else None
    ev = mcap + (debt or 0) - (cash or 0) if mcap is not None else None
    m = {
        "market_cap": mcap,
        "pe_ttm": _div(mcap, ni), "pb": _div(mcap, equity), "ps": _div(mcap, rev),
        "ev_ebitda": _div(ev, ebitda),
        "roe": _div(ni, equity), "roa": _div(ni, assets),
        "gross_margin": _div(gp, rev), "op_margin": _div(oi, rev), "net_margin": _div(ni, rev),
        "debt_equity": _div(debt, equity), "current_ratio": _div(cur_a, cur_l),
        "div_yield": (div12 / price) if price else None,
        "payout": _div(div12 * shares, ni) if shares else None,
        "revenue_ttm": rev, "net_income_ttm": ni, "fcf_ttm": fcf,
        "rev_growth_yoy": yoy(income, "Total Revenue", "Operating Revenue"),
        "eps_growth_yoy": yoy(income, "Net Income", "Net Income Common Stockholders"),
    }
    # roe boleh negatif (laba rugi), tetapi ekuitas harus positif (ditangani _div)
    if ni is not None and equity is not None and equity > 0:
        m["roe"] = ni / equity
    for col, (lo, hi) in LIMITS.items():            # sanity check bagian 6
        if m[col] is not None and not (lo < m[col] < hi):
            m[col] = None

    has_data = any(v is not None for v in (rev, ni, equity, assets))
    na: dict[str, str] = {}
    for col, v in m.items():
        if v is not None or col == "market_cap":
            continue
        if is_financial and col in FIN_NA:
            na[col] = "bank"
        elif not has_data:
            na[col] = "no data"
        elif col in LOSS_COLS and ni is not None and ni <= 0:
            na[col] = "loss"
        else:
            na[col] = "n/a"
    clean = {c: (None if v is None or (isinstance(v, float) and not math.isfinite(v)) else float(v))
             for c, v in m.items()}
    return {**clean, "na_reason": na}
