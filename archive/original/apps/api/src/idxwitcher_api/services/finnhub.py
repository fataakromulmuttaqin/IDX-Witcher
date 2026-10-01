"""Finnhub fallback client for company fundamentals.

Used as secondary source when Yahoo Finance fundamentals are sparse.
"""

from __future__ import annotations

import logging
from decimal import Decimal

import httpx

log = logging.getLogger(__name__)

BASE_URL = "https://finnhub.io/api/v1"


class FinnhubClient:
    """Thin wrapper around Finnhub public REST API."""

    def __init__(self, api_key: str | None = None, timeout: float = 30.0):
        self.api_key = api_key
        self.timeout = timeout
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(timeout=self.timeout, base_url=BASE_URL)
        return self._client

    def _get(self, endpoint: str, params: dict | None = None) -> dict | None:
        if not self.api_key:
            log.debug("Finnhub API key not configured")
            return None
        params = params or {}
        params["token"] = self.api_key
        try:
            response = self.client.get(endpoint, params=params)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 429:
                log.warning("Finnhub rate limit hit for %s", endpoint)
            else:
                log.debug("Finnhub HTTP %d for %s", response.status_code, endpoint)
            return None
        except Exception as exc:
            log.debug("Finnhub request error: %s", exc)
            return None

    def company_profile(self, symbol: str) -> dict | None:
        """Fetch company profile 2 (free endpoint)."""
        return self._get("/stock/profile2", {"symbol": f"{symbol.upper()}.JK"})

    def basic_financials(self, symbol: str) -> dict | None:
        """Fetch basic financial metrics."""
        return self._get("/stock/metric", {"symbol": f"{symbol.upper()}.JK", "metric": "all"})

    def quote(self, symbol: str) -> dict | None:
        """Fetch real-time quote."""
        return self._get("/quote", {"symbol": f"{symbol.upper()}.JK"})


def normalize_finnhub_profile(data: dict) -> dict:
    """Normalize Finnhub profile2 response into IDX Witcher company fields."""
    if not data:
        return {}

    market_cap = data.get("marketCapitalization")
    if market_cap is not None:
        # Finnhub reports market cap in millions for some regions; try to infer IDR
        market_cap = int(market_cap) * 1_000_000

    share_outstanding = data.get("shareOutstanding")
    if share_outstanding is not None:
        share_outstanding = int(share_outstanding)

    return {
        "name": data.get("name") or data.get("ticker"),
        "sector": data.get("finnhubIndustry"),
        "currency": data.get("currency"),
        "ipo": data.get("ipo"),
        "market_cap": market_cap,
        "shares": share_outstanding,
        "website": data.get("weburl"),
        "logo": data.get("logo"),
        "country": data.get("country"),
        "exchange": data.get("exchange"),
    }


def normalize_finnhub_financials(data: dict) -> dict:
    """Normalize Finnhub basic financials into common fields."""
    if not data:
        return {}

    metrics = data.get("metric", {}) if isinstance(data, dict) else {}

    def to_decimal(value):
        if value is None or value == "":
            return None
        try:
            return Decimal(str(value))
        except Exception:
            return None

    return {
        "pe_ratio": to_decimal(metrics.get("peTTM")),
        "forward_pe": to_decimal(metrics.get("peNormalizedAnnual")),
        "eps_trailing": to_decimal(metrics.get("epsTTM")),
        "dividend_yield": to_decimal(metrics.get("dividendYieldIndicatedAnnual")),
        "pb_ratio": to_decimal(metrics.get("pbAnnual")),
        "roe": to_decimal(metrics.get("roeTTM")),
        "profit_margin": to_decimal(metrics.get("netProfitMarginTTM")),
        "52_week_high": to_decimal(metrics.get("52WeekHigh")),
        "52_week_low": to_decimal(metrics.get("52WeekLow")),
    }
