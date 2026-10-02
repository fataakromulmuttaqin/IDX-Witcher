import time
from datetime import date, timedelta

import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import FinancialStatement, FundamentalsSnapshot
from providers.base import DataProvider
from providers.yahoo import YahooProvider
from worker.fundamentals import compute_snapshot
from worker.runlog import logged_run

FAIL_TOLERANCE = 0.30


def _usd_idr(provider: DataProvider) -> float | None:
    df = provider.fetch_prices(["IDR=X"], start=(date.today() - timedelta(days=10)).isoformat())
    if df.empty or "close" not in df.columns:
        return None
    s = pd.to_numeric(df.sort_values("date")["close"], errors="coerce").dropna()
    return float(s.iloc[-1]) if len(s) else None


def _stmt_rows(ticker: str, df: pd.DataFrame | None, stmt: str, currency: str) -> list[dict]:
    rows: list[dict] = []
    if df is None or df.empty:
        return rows
    for item in df.index:
        series = pd.to_numeric(df.loc[item], errors="coerce")
        for col, v in series.items():
            if pd.notna(v):
                rows.append({"ticker": ticker, "period_end": pd.Timestamp(col).date(),
                             "period_type": "Q", "statement": stmt, "item": str(item),
                             "value": float(v), "currency": currency, "source": "yfinance"})
    return rows


def run(provider: DataProvider | None = None, limit: int | None = None) -> dict:
    provider = provider or YahooProvider()
    with logged_run("fundamentals") as res:
        with SessionLocal() as s:
            companies = s.execute(text("""
                SELECT c.ticker, c.yahoo_symbol, c.shares_outstanding, c.is_financial,
                       (SELECT close FROM prices_daily p WHERE p.ticker = c.ticker
                        ORDER BY trade_date DESC LIMIT 1) AS close
                FROM companies c WHERE c.is_active ORDER BY c.ticker""")).mappings().all()
            div12 = dict(s.execute(text("""
                SELECT ticker, sum(value) FROM corporate_actions
                WHERE kind = 'dividend' AND action_date >= CURRENT_DATE - 365
                GROUP BY ticker""")).all())
            fx = _usd_idr(provider)
            failed = 0
            todo = companies[:limit] if limit else companies
            for n, c in enumerate(todo, start=1):
                try:
                    data = provider.fetch_fundamentals(c["yahoo_symbol"])
                except Exception:  # noqa: BLE001
                    failed += 1
                    continue
                info = data.get("info") or {}
                shares = info.get("sharesOutstanding") or c["shares_outstanding"]
                if shares and shares != c["shares_outstanding"]:
                    s.execute(text("UPDATE companies SET shares_outstanding = :sh WHERE ticker = :t"),
                              {"sh": int(shares), "t": c["ticker"]})
                snap = compute_snapshot(
                    price=float(c["close"]) if c["close"] is not None else None,
                    shares=int(shares) if shares else None, is_financial=c["is_financial"],
                    info=info, income=data.get("income"), balance=data.get("balance"),
                    cashflow=data.get("cashflow"), fx=fx, div12=float(div12.get(c["ticker"], 0.0)))
                res["rows"] += upsert(s, FundamentalsSnapshot,
                                      [{"ticker": c["ticker"], "as_of": date.today(), **snap}],
                                      ["ticker", "as_of"])
                cur = info.get("financialCurrency") or "IDR"
                stmts = (_stmt_rows(c["ticker"], data.get("income"), "IS", cur)
                         + _stmt_rows(c["ticker"], data.get("balance"), "BS", cur)
                         + _stmt_rows(c["ticker"], data.get("cashflow"), "CF", cur))
                upsert(s, FinancialStatement, stmts,
                       ["ticker", "period_end", "period_type", "statement", "item"])
                if n % 50 == 0:
                    s.commit()
                time.sleep(0.5)
            s.commit()
            res["failed"] = failed
            if todo and failed / len(todo) > FAIL_TOLERANCE:
                raise RuntimeError(f"{failed} dari {len(todo)} emiten gagal")
    return res
