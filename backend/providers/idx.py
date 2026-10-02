"""
IDX.co.id provider — spike stub untuk analisis laporan keuangan.

Sumber: idx.co.id/primary/FinancialStatementOfIssuer/GetFinancialStatement
        + instance.zip / FinancialStatement-*.xlsx per emiten per kuartal.

Status: STUB — implementasi bertahap:
  Fase A: parse XLSX manual upload (paling cepat, tanpa WAF)
  Fase B: hit XHR API dengan header+cookie bypass
  Fase C: parse instance.zip XBRL → long format

Mapping: lihat xbrl_map.yaml (ifrs-full:Revenue → TotalRevenue dll).

Tidak dipakai pipeline harian sampai di-approve. Slot sesuai PRD §6 & §14.7.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd

from providers.base import DataProvider

# Base URL idx.co.id — sama dengan archive/original idx_client.py
BASE_URL = "https://www.idx.co.id/primary"
DEFAULT_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "referer": "https://www.idx.co.id/id/perusahaan-tercatat/laporan-keuangan-dan-tahunan",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
}

# Endpoint LK (ditemukan dari extract + network sniffing)
# POST /primary/FinancialStatementOfIssuer/GetFinancialStatement?year=YYYY&period=I|II|III&kodeEmiten=XXXX
LK_PERIODS = {"I": "Q1", "II": "Q2", "III": "Q3", "Tahunan": "FY"}

# Mapping IFRS → internal item (diisi bertahap, lihat spike doc)
XBRL_MAP: dict[str, str] = {
    # placeholder — isi setelah inspeksi instance.zip BBCA
    "ifrs-full:Revenue": "TotalRevenue",
    "ifrs-full:ProfitLoss": "NetIncome",
    "ifrs-full:Assets": "TotalAssets",
    "ifrs-full:Equity": "StockholdersEquity",
    "ifrs-full:CashAndCashEquivalents": "CashAndCashEquivalents",
}


class IDXProvider(DataProvider):
    """Provider untuk laporan keuangan resmi idx.co.id.

    Untuk MVP, cukup pakai parse_xlsx() dari file manual.
    fetch_prices/fetch_actions/fetch_fundamentals didelegasikan ke Yahoo
    (IDX tidak dipakai untuk harga harian).
    """

    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or Path(__file__).resolve().parent.parent / "data" / "idx_reports"

    # --- DataProvider interface (stub, delegasi ke Yahoo untuk harga) ---

    def fetch_prices(self, symbols: list[str], start: str, end: str | None = None) -> pd.DataFrame:  # type: ignore[override]
        raise NotImplementedError("IDX tidak dipakai untuk harga harian — pakai YahooProvider")

    def fetch_actions(self, symbols: list[str]) -> pd.DataFrame:  # type: ignore[override]
        raise NotImplementedError("IDX tidak dipakai untuk corporate actions — pakai YahooProvider")

    def fetch_fundamentals(self, symbol: str) -> dict:  # type: ignore[override]
        raise NotImplementedError("Gunakan import_idx_reports untuk LK IDX, bukan per-symbol fetch")

    # --- Fase A: XLSX manual ---

    def parse_xlsx(self, xlsx_path: Path | str, ticker: str) -> list[dict[str, Any]]:
        """Parse FinancialStatement-YYYY-P-XXXX.xlsx → list rows untuk financial_statements.

        Returns: [{ticker, period_end, period_type, statement, item, value, currency, source}]
        """
        xlsx_path = Path(xlsx_path)
        # TODO: inspect sheet names dari contoh BBCA — biasanya "Laporan Laba Rugi", "Neraca" dll.
        # Stub: baca semua sheet, mapping belum final
        xls = pd.ExcelFile(xlsx_path)
        rows: list[dict[str, Any]] = []
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            # TODO: mapping kolom → item (butuh sampel file asli)
            _ = df  # placeholder
        return rows

    # --- Fase C: XBRL ZIP ---

    def parse_instance_zip(self, zip_bytes: bytes, ticker: str) -> list[dict[str, Any]]:
        """Parse instance.zip (XBRL) → long format rows."""
        rows: list[dict[str, Any]] = []
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            for name in zf.namelist():
                if name.endswith((".xml", ".xbrl")):
                    xml = zf.read(name)
                    # TODO: xml.etree.ElementTree parse + XBRL_MAP
                    _ = xml
        return rows

    # --- Fase B: XHR listing (butuh bypass Cloudflare) ---

    def fetch_report_list(
        self, year: int, period: str, kode_emiten: str | None = None
    ) -> list[dict[str, Any]]:
        """Hit GetFinancialStatement — butuh header+cookie yang lolos WAF.

        period: I, II, III, Tahunan
        Returns: [{ticker, year, period, files: {xlsx, instance, pdf}}]
        """
        # TODO: implement dengan httpx + cookie jar + retry
        # Lihat archive/original idx_client.py untuk pola headers/retry
        raise NotImplementedError("Butuh bypass Cloudflare — implement setelah spike B di-approve")


# --- Helper: konversi ke format financial_statements (dipakai worker) ---


def to_long_rows(
    ticker: str,
    period_end: str,
    statement: str,
    items: dict[str, float],
    currency: str = "IDR",
) -> list[dict[str, Any]]:
    """Bungkus dict {item: value} → rows untuk upsert ke financial_statements."""
    from datetime import date as _date

    # period_end bisa "2026-03-31" atau date
    pe = _date.fromisoformat(period_end) if isinstance(period_end, str) else period_end
    ptype = "Q"  # TODO: tentukan Q vs FY dari period
    return [
        {
            "ticker": ticker,
            "period_end": pe,
            "period_type": ptype,
            "statement": statement,
            "item": item,
            "value": value,
            "currency": currency,
            "source": "idx",
        }
        for item, value in items.items()
        if value is not None
    ]
