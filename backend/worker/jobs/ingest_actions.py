from sqlalchemy import select

from core.db import SessionLocal, upsert
from core.models import Company, CorporateAction
from providers.base import DataProvider
from providers.yahoo import YahooProvider
from worker.runlog import logged_run


def run(provider: DataProvider | None = None) -> dict:
    provider = provider or YahooProvider()
    with logged_run("actions") as res, SessionLocal() as s:
        symbols = list(s.scalars(select(Company.yahoo_symbol).where(Company.is_active)))
        df = provider.fetch_actions(symbols)
        if df.empty:
            return res
        df["ticker"] = df["symbol"].str.removesuffix(".JK")
        rows = [
            {"ticker": r.ticker, "action_date": r.date, "kind": r.kind, "value": r.value}
            for r in df.itertuples()
        ]
        res["rows"] = upsert(s, CorporateAction, rows, ["ticker", "action_date", "kind"])
        s.commit()
    return res
