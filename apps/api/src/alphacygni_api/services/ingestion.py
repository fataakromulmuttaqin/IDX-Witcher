"""Data ingestion orchestration with fallback."""

import logging
from typing import Sequence

from sqlalchemy.orm import Session

from IDX Witcher_api.services.idx_client import IDXClient
from IDX Witcher_api.services.yahoo import YahooFinanceClient
from IDX Witcher_api.db.models import Company, OHLCV, MarketSummary

log = logging.getLogger(__name__)

# Default LQ45 constituents as seed (can be replaced with dynamic fetch later)
DEFAULT_LQ45 = [
    "ACES", "ADRO", "AKR", "AMMN", "AMRT", "ANTM", "ARTO", "ASII", "BBCA", "BBNI",
    "BBRI", "BMRI", "BRMS", "BRPT", "BTPN", "CAMP", "CARE", "CEPU", "CMRY", "CPIN",
    "DCII", "DMAS", "DOID", "DSFI", "ELSA", "EXCL", "GGRM", "GJTL", "GOTO", "HRUM",
    "ICBP", "INCO", "INDF", "INKP", "INTP", "ITMG", "JPFA", "JSMR", "KLBF", "MAPI",
    "MBMA", "MEDC", "MIKA", "MNCN", "MTEL",
]


class IngestionService:
    """Ingest market data with primary source and fallback."""

    def __init__(self, db: Session):
        self.db = db
        self.idx_client = IDXClient()
        self.yahoo_client = YahooFinanceClient()

    def seed_companies(self) -> int:
        """Ensure default LQ45 companies exist in DB."""
        count = 0
        for code in DEFAULT_LQ45:
            existing = self.db.query(Company).filter(Company.code == code).first()
            if existing is None:
                self.db.add(Company(code=code, name=code, is_active=True, source="seed"))
                count += 1
        self.db.commit()
        log.info("Seeded %d companies", count)
        return count

    def ingest_ohlcv_yahoo(self, code: str, period: str = "1y") -> int:
        """Ingest OHLCV from Yahoo Finance for one ticker."""
        records = self.yahoo_client.fetch_ohlcv(code, period=period)
        if not records:
            return 0

        count = 0
        for rec in records:
            existing = (
                self.db.query(OHLCV)
                .filter(OHLCV.code == rec["code"], OHLCV.date == rec["date"])
                .first()
            )
            if existing:
                continue
            self.db.add(OHLCV(**rec))
            count += 1
        self.db.commit()
        log.info("Inserted %d Yahoo OHLCV rows for %s", count, code)
        return count

    def ingest_ohlcv_batch(self, codes: Sequence[str], period: str = "1y") -> dict:
        """Ingest OHLCV for multiple tickers."""
        results = {}
        for code in codes:
            try:
                n = self.ingest_ohlcv_yahoo(code, period=period)
                results[code] = n
            except Exception as exc:
                log.exception("Failed to ingest %s: %s", code, exc)
                results[code] = -1
        return results

    def ingest_market_summary(self, index_code: str = "^JKSE", period: str = "1y") -> int:
        """Ingest market/index summary from Yahoo Finance."""
        records = self.yahoo_client.fetch_market_summary(index_code, period=period)
        if not records:
            return 0

        count = 0
        for rec in records:
            existing = (
                self.db.query(MarketSummary)
                .filter(MarketSummary.date == rec["date"], MarketSummary.index_code == rec["index_code"])
                .first()
            )
            if existing:
                continue
            self.db.add(MarketSummary(**rec))
            count += 1
        self.db.commit()
        log.info("Inserted %d market summary rows for %s", count, index_code)
        return count
