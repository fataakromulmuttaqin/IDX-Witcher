"""Simple IDX HTTP client for public endpoints."""

import json
import logging
from datetime import date, datetime
from decimal import Decimal

import httpx

log = logging.getLogger(__name__)

BASE_URL = "https://www.idx.co.id/primary"
DEFAULT_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://www.idx.co.id/",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
}

RETRYABLE_STATUS = (403, 429, 500, 502, 503, 504)


class IDXClient:
    """Thin wrapper around httpx for IDX public endpoints with simple retry."""

    def __init__(self, base_url: str = BASE_URL, timeout: float = 30.0, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(headers=DEFAULT_HEADERS, timeout=self.timeout)
        return self._client

    def get(self, endpoint: str, params: dict | None = None) -> dict | None:
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}{endpoint}"
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.get(url, params=params)
                if response.status_code == 200:
                    return response.json()
                if response.status_code in RETRYABLE_STATUS and attempt < self.max_retries:
                    log.warning("HTTP %d for %s, retrying...", response.status_code, url)
                    continue
                log.error("HTTP %d for %s", response.status_code, url)
                return None
            except json.JSONDecodeError as exc:
                log.error("JSON decode error for %s: %s", url, exc)
                return None
            except Exception as exc:  # noqa: BLE001
                log.warning("Request error for %s: %s", url, exc)
                if attempt < self.max_retries:
                    continue
                return None
        return None

    def fetch_stock_summary(self, date_str: str | None = None, start: int = 0, length: int = 9999) -> dict | None:
        if date_str is None:
            date_str = datetime.now().strftime("%Y%m%d")
        return self.get("/TradingSummary/GetStockSummary", {"date": date_str, "start": start, "length": length})

    def fetch_broker_summary(self, date_str: str | None = None, start: int = 0, length: int = 9999) -> dict | None:
        if date_str is None:
            date_str = datetime.now().strftime("%Y%m%d")
        return self.get("/TradingSummary/GetBrokerSummary", {"date": date_str, "start": start, "length": length})

    def fetch_index_summary(self, date_str: str | None = None, start: int = 0, length: int = 9999) -> dict | None:
        if date_str is None:
            date_str = datetime.now().strftime("%Y%m%d")
        return self.get("/TradingSummary/GetIndexSummary", {"date": date_str, "start": start, "length": length})

    def fetch_company_profiles(self, start: int = 0, length: int = 9999) -> dict | None:
        return self.get("/Helper/GetCompanyProfiles", {"start": start, "length": length})


def normalize_idx_ohlcv(data: dict, as_of_date: date | None = None) -> list[dict]:
    """Normalize raw IDX stock summary response into OHLCV records."""
    if not data or "data" not in data:
        return []
    if as_of_date is None:
        as_of_date = date.today()

    records = []
    for row in data.get("data", []):
        try:
            records.append(
                {
                    "code": str(row["StockCode"]).upper(),
                    "date": as_of_date,
                    "open_price": _to_decimal(row.get("OpenPrice")),
                    "high_price": _to_decimal(row.get("HighPrice")),
                    "low_price": _to_decimal(row.get("LowPrice")),
                    "close_price": _to_decimal(row.get("ClosePrice")),
                    "volume": _to_int(row.get("Volume")),
                    "value": _to_decimal(row.get("Value")),
                    "frequency": _to_int(row.get("Frequency")),
                    "source": "idx",
                }
            )
        except (KeyError, ValueError) as exc:
            log.debug("Skipping malformed IDX row: %s (%s)", row, exc)
            continue
    return records


def _to_decimal(value):
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))  # noqa: F821
    except Exception:
        return None


def _to_int(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except Exception:
        return None
