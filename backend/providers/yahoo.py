import random
import time

import pandas as pd
import yfinance as yf

from core.config import get_settings
from providers.base import DataProvider

COLS = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
}


def _retry(fn, attempts: int = 3, base: float = 2.0):
    for i in range(attempts):
        try:
            return fn()
        except Exception:
            if i == attempts - 1:
                raise
            time.sleep(base ** (i + 1) + random.random())


class YahooProvider(DataProvider):
    def fetch_prices(self, symbols, start, end=None):
        cfg = get_settings()
        frames: list[pd.DataFrame] = []
        failed: list[str] = []
        for i in range(0, len(symbols), cfg.yahoo_batch_size):
            batch = symbols[i : i + cfg.yahoo_batch_size]
            try:
                raw = _retry(
                    lambda: yf.download(
                        batch,
                        start=start,
                        end=end,
                        auto_adjust=False,
                        group_by="ticker",
                        threads=True,
                        progress=False,
                    )
                )
            except Exception:
                failed.extend(batch)
                continue
            level0 = raw.columns.get_level_values(0) if isinstance(raw.columns, pd.MultiIndex) else []
            for sym in batch:
                if sym not in level0:
                    failed.append(sym)
                    continue
                df = raw[sym].dropna(how="all")
                if df.empty:
                    failed.append(sym)
                    continue
                df = df.rename(columns=COLS).reset_index()
                df = df.rename(columns={df.columns[0]: "date"})
                df["symbol"] = sym
                df["date"] = pd.to_datetime(df["date"]).dt.date
                frames.append(df[["symbol", "date", *COLS.values()]])
            time.sleep(cfg.yahoo_batch_sleep)
        out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
            columns=["symbol", "date", *COLS.values()])
        out.attrs["failed"] = failed
        return out

    def fetch_actions(self, symbols):
        rows = []
        for sym in symbols:
            try:
                act = _retry(lambda: yf.Ticker(sym).actions)
            except Exception:
                continue
            for ts, r in act.iterrows():
                if r.get("Dividends", 0) > 0:
                    rows.append((sym, ts.date(), "dividend", float(r["Dividends"])))
                if r.get("Stock Splits", 0) > 0:
                    rows.append((sym, ts.date(), "split", float(r["Stock Splits"])))
            time.sleep(0.3)
        return pd.DataFrame(rows, columns=["symbol", "date", "kind", "value"])

    def fetch_fundamentals(self, symbol):
        t = yf.Ticker(symbol)
        return {
            "info": _retry(lambda: t.info) or {},
            "income": t.quarterly_income_stmt,
            "balance": t.quarterly_balance_sheet,
            "cashflow": t.quarterly_cashflow,
        }
