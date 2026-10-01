"""Investing.com fallback scraper for Indonesian stocks.

Lightweight HTML scraper for summary stats, fundamentals, and quote.
"""

from __future__ import annotations

import logging
import re
from decimal import Decimal
from typing import Any

import httpx
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

BASE_URL = "https://id.investing.com/equities"


class InvestingClient:
    """Client to fetch Indonesian equity data from Investing.com."""

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/128.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
            self._client = httpx.Client(headers=headers, timeout=self.timeout)
        return self._client

    def _get(self, path: str) -> BeautifulSoup | None:
        url = f"{BASE_URL}/{path}"
        try:
            response = self.client.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            log.debug("Investing.com HTTP %d for %s", response.status_code, url)
            return None
        except Exception as exc:
            log.debug("Investing.com request error: %s", exc)
            return None

    def _normalize_ticker(self, code: str) -> str:
        code = code.upper().replace(".JK", "")
        # Known Investing.com slug patterns for major IDX stocks
        mapping = {
            "BBCA": "bank-central-asia",
            "BBRI": "bank-rakyat-indonesia",
            "BMRI": "bank-mandiri",
            "BBNI": "bank-negara-indonesia",
            "TLKM": "telekomunikasi-indonesia",
            "ASII": "astra-international",
            "INDF": "indofood-sukses-makmur",
            "UNVR": "unilever-indonesia",
            "ICBP": "indofood-cbp-sukses-makmur",
            "ANTM": "aneka-tambang",
            "PTBA": "bukit-asam",
            "TPIA": "chandra-asri-petrochemical",
            "GOTO": "go-to-gojek-tokopedia",
            "BBTN": "bank-tabungan-negara",
            "BMTR": "bakrie-telecom",
            "EXCL": "XL-axiata",
            "ISAT": "indosat",
            "PGAS": "perusahaan-gas-negara",
            "SMBR": "semen-baturaja",
            "SMGR": "semen-indonesia",
            "WIKA": "wijaya-karya",
            "WSKT": "waskita-karya",
        }
        return mapping.get(code, code.lower())

    def fetch_quote(self, code: str) -> dict[str, Any] | None:
        """Fetch current quote and key stats from Investing.com."""
        slug = self._normalize_ticker(code)
        soup = self._get(slug)
        if not soup:
            return None

        data: dict[str, Any] = {"source": "investing.com", "code": code.upper()}

        # Last price
        price_selectors = [
            "span.text-5xl",
            "span.instrument-price_last__",
            "div.instrument-price",
            "span[data-test='instrument-price-last']",
        ]
        for selector in price_selectors:
            el = soup.select_one(selector)
            if el:
                data["last_price"] = _to_decimal(_clean_text(el.get_text()))
                break

        # Stats table
        stats: dict[str, Any] = {}
        for row in soup.select("div.instrument-data_table__rows__") or []:
            cells = row.find_all("div", recursive=False)
            if len(cells) >= 2:
                key = _clean_text(cells[0].get_text()).lower()
                value = _clean_text(cells[1].get_text())
                stats[key] = value
        data["stats"] = stats

        # Fallback fundamental extraction from stats text
        data["pe_ratio"] = _to_decimal(stats.get("p/e ratio")) or _to_decimal(stats.get("rasio p/e"))
        data["eps"] = _to_decimal(stats.get("eps")) or _to_decimal(stats.get("eps (ttm)"))
        data["dividend_yield"] = _to_decimal(stats.get("dividend yield")) or _to_decimal(stats.get("hasil dividen"))
        data["market_cap"] = _to_decimal(stats.get("market cap")) or _to_decimal(stats.get("kapitalisasi pasar"))

        return data


def _clean_text(text: str | None) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def _to_decimal(value):
    if value is None or value == "":
        return None
    text = str(value).replace(",", "").replace("%", "").strip()
    if text in ("-", "N/A", "n/a"):
        return None
    try:
        return Decimal(text)
    except Exception:
        return None
