"""TradingView scanner API client for IDX market data.

Unofficial API: https://scanner.tradingview.com/indonesia/scan
Provides real-time quotes, fundamentals, and technical indicators
for all IDX-listed stocks.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx

log = logging.getLogger(__name__)

SCANNER_URL = "https://scanner.tradingview.com/indonesia/scan"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Columns available from TradingView scanner for IDX stocks
STOCK_COLUMNS = [
    "name",
    "description",
    "close",
    "change",
    "volume",
    "market_cap_basic",
    "sector",
    "industry",
    "price_earnings_ttm",
    "earnings_per_share_basic_ttm",
    "dividend_yield_recent",
    "price_book_ratio",
    "return_on_equity",
    "debt_to_equity",
    "gross_margin",
    "net_margin",
    "total_revenue",
    "net_income",
    "beta_1_year",
    "price_52_week_high",
    "price_52_week_low",
    "RSI",
    "RSI[1]",
    "MACD.macd",
    "EMA20",
    "EMA50",
    "EMA200",
    "SMA20",
    "SMA50",
    "ATR",
    "Volatility.D",
]


class TradingViewClient:
    """Client for TradingView Indonesia scanner API."""

    def __init__(self, timeout: float = 60.0):
        self.timeout = timeout
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(headers=DEFAULT_HEADERS, timeout=self.timeout)
        return self._client

    def _post(self, payload: dict) -> dict | None:
        try:
            response = self.client.post(SCANNER_URL, json=payload)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 429:
                log.warning("TradingView rate limit hit")
            else:
                log.error("TradingView scanner HTTP %d: %s", response.status_code, response.text[:200])
            return None
        except Exception as exc:
            log.exception("TradingView scanner request failed: %s", exc)
            return None

    def scan_all_stocks(
        self,
        columns: list[str] | None = None,
        limit: int | None = None,
        min_market_cap: float | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch all IDX stocks from TradingView scanner."""
        payload: dict[str, Any] = {
            "filter": [{"left": "type", "operation": "equal", "right": "stock"}],
            "options": {"lang": "en"},
            "columns": columns or STOCK_COLUMNS,
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
        }
        if min_market_cap is not None:
            payload["filter"].append(
                {"left": "market_cap_basic", "operation": "egreater", "right": min_market_cap}
            )

        if limit and limit <= 250:
            payload["range"] = [0, limit]
            data = self._post(payload)
            if not data:
                return []
            return _normalize_scanner_data(data, payload["columns"])

        # Paginate all results
        results: list[dict[str, Any]] = []
        start = 0
        page_size = 250
        while True:
            payload["range"] = [start, start + page_size]
            data = self._post(payload)
            if not data:
                break
            rows = _normalize_scanner_data(data, payload["columns"])
            if not rows:
                break
            results.extend(rows)
            if limit and len(results) >= limit:
                return results[:limit]
            if len(rows) < page_size:
                break
            start += page_size

        return results

    def quote(self, ticker: str, columns: list[str] | None = None) -> dict[str, Any] | None:
        """Fetch single ticker data from TradingView scanner."""
        tv_symbol = f"IDX:{ticker.upper().replace('.JK', '')}"
        payload = {
            "symbols": {"tickers": [tv_symbol], "query": {"types": []}},
            "columns": columns or STOCK_COLUMNS,
        }
        data = self._post(payload)
        if not data or not data.get("data"):
            return None
        rows = _normalize_scanner_data(data, payload["columns"])
        return rows[0] if rows else None


def _normalize_scanner_data(data: dict, columns: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in data.get("data", []):
        symbol = item.get("s", "")
        ticker = symbol.replace("IDX:", "")
        row: dict[str, Any] = {"ticker": ticker, "tv_symbol": symbol, "timestamp_utc": datetime.now(timezone.utc).isoformat()}
        values = item.get("d", [])
        for col, val in zip(columns, values):
            row[col] = val
        rows.append(row)
    return rows
