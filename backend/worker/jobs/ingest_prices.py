from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select

from core.db import SessionLocal, upsert
from core.models import Company, PriceDaily
from providers.base import DataProvider
from providers.yahoo import YahooProvider
from worker.quality import flag_suspect
from worker.runlog import logged_run

FAIL_TOLERANCE = 0.05


def run(provider: DataProvider | None = None, lookback_days: int = 10,
        start: str | None = None) -> dict:
    provider = provider or YahooProvider()
    today = datetime.now(ZoneInfo("Asia/Jakarta")).date()
    start = start or (today - timedelta(days=lookback_days)).isoformat()
    with logged_run("prices") as res, SessionLocal() as s:
        symbols = list(s.scalars(select(Company.yahoo_symbol).where(Company.is_active)))
        df = provider.fetch_prices(symbols, start=start)
        failed = df.attrs.get("failed", [])
        res["failed"] = len(failed)
        if symbols and len(failed) / len(symbols) > FAIL_TOLERANCE:
            raise RuntimeError(f"{len(failed)} dari {len(symbols)} ticker gagal")
        if df.empty:
            return res
        df["ticker"] = df["symbol"].str.removesuffix(".JK")
        df = df.dropna(subset=["close"]).copy()
        df["value_traded"] = df["close"] * df["volume"].fillna(0)
        df["is_suspect"] = flag_suspect(df)
        cols = ["ticker", "date", "open", "high", "low", "close", "adj_close",
                "volume", "value_traded", "is_suspect"]
        out = df[cols].rename(columns={"date": "trade_date"})
        out = out.astype(object).where(out.notna(), None)
        res["rows"] = upsert(s, PriceDaily, out.to_dict("records"), ["ticker", "trade_date"])
        s.commit()
    return res
