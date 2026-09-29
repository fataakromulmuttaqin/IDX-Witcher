"""Yahoo Finance fallback scraper for IDX stocks."""

import logging
from datetime import date, datetime
from decimal import Decimal

import yfinance as yf

log = logging.getLogger(__name__)


class YahooFinanceClient:
    """Wrapper around yfinance to fetch Indonesian stocks (.JK suffix)."""

    def __init__(self, session: yf.Ticker | None = None):
        self.session = session  # reserved for custom session

    def _ticker(self, code: str) -> yf.Ticker:
        return yf.Ticker(f"{code.upper()}.JK")

    def fetch_ohlcv(self, code: str, period: str = "1y") -> list[dict]:
        """Fetch daily OHLCV for a single ticker."""
        ticker = self._ticker(code)
        hist = ticker.history(period=period)
        if hist is None or hist.empty:
            log.warning("No Yahoo data for %s", code)
            return []

        records = []
        for dt, row in hist.iterrows():
            records.append(
                {
                    "code": code.upper(),
                    "date": dt.date() if hasattr(dt, "date") else dt,
                    "open_price": _to_decimal(row.get("Open")),
                    "high_price": _to_decimal(row.get("High")),
                    "low_price": _to_decimal(row.get("Low")),
                    "close_price": _to_decimal(row.get("Close")),
                    "volume": _to_int(row.get("Volume")),
                    "value": None,
                    "frequency": None,
                    "source": "yahoo",
                }
            )
        return records

    def fetch_market_summary(self, index_code: str = "^JKSE", period: str = "1y") -> list[dict]:
        """Fetch market/index summary (e.g., IHSG = ^JKSE)."""
        ticker = yf.Ticker(index_code)
        hist = ticker.history(period=period)
        if hist is None or hist.empty:
            return []

        records = []
        for dt, row in hist.iterrows():
            records.append(
                {
                    "date": dt.date() if hasattr(dt, "date") else dt,
                    "index_code": index_code,
                    "index_name": _index_name(index_code),
                    "open_value": _to_decimal(row.get("Open")),
                    "high_value": _to_decimal(row.get("High")),
                    "low_value": _to_decimal(row.get("Low")),
                    "close_value": _to_decimal(row.get("Close")),
                    "change": None,
                    "change_percent": None,
                    "volume": _to_int(row.get("Volume")),
                    "value": None,
                    "source": "yahoo",
                }
            )
        return records


def _to_decimal(value):
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except Exception:
        return None


def _to_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


def _index_name(code: str) -> str:
    mapping = {
        "^JKSE": "IHSG",
        "^JKL45": "LQ45",
    }
    return mapping.get(code, code)
