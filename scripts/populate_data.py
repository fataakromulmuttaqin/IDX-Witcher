"""CLI to populate IDX Witcher database with complete data.

Usage:
    python -m scripts.populate_data
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps/api/src"))

from idxwitcher_api.db.session import SessionLocal
from idxwitcher_api.services.ingestion import IngestionService
from idxwitcher_api.services.tv_sync import sync_companies_from_tradingview


def main():
    db = SessionLocal()
    try:
        print("Syncing companies from TradingView...")
        result = sync_companies_from_tradingview(db)
        print(f"Synced {result['total_synced']} companies ({result['created']} created, {result['updated']} updated)")

        print("Seeding LQ45 defaults...")
        service = IngestionService(db)
        service.seed_companies()

        print("Ingesting IHSG market summary...")
        service.ingest_market_summary("^JKSE", period="5y")

        print("Ingesting OHLCV for LQ45...")
        lq45 = [
            "ACES", "ADRO", "AKR", "AMMN", "AMRT", "ANTM", "ARTO", "ASII", "BBCA", "BBNI",
            "BBRI", "BMRI", "BRMS", "BRPT", "BTPN", "CAMP", "CARE", "CEPU", "CMRY", "CPIN",
            "DCII", "DMAS", "DOID", "DSFI", "ELSA", "EXCL", "GGRM", "GJTL", "GOTO", "HRUM",
            "ICBP", "INCO", "INDF", "INKP", "INTP", "ITMG", "JPFA", "JSMR", "KLBF", "MAPI",
            "MBMA", "MEDC", "MIKA", "MNCN", "MTEL", "PTBA", "SMGR", "TINS", "TLKM", "TPIA",
            "UNTR", "UNVR",
        ]
        for code in lq45:
            try:
                rows = service.ingest_ohlcv_yahoo(code, period="5y")
                print(f"  {code}: {rows} rows")
            except Exception as exc:
                print(f"  {code}: failed ({exc})")

        print("Done.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
