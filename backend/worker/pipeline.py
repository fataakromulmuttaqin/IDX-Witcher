import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx

from core.cache import purge
from core.config import get_settings
from providers.yahoo import YahooProvider
from worker.jobs import compute_indicators, ingest_fundamentals, ingest_prices, run_rules
from worker.jobs.seed_rules import run as seed_rules

log = logging.getLogger("pipeline")
WIB = ZoneInfo("Asia/Jakarta")


def market_open_today(provider) -> bool:
    today = datetime.now(WIB).date()
    df = provider.fetch_prices(["^JKSE"], start=(today - timedelta(days=7)).isoformat())
    return (not df.empty) and df["date"].max() == today


def alert(message: str) -> None:
    log.error(message)
    url = get_settings().alert_webhook_url
    if url:
        try:
            httpx.post(url, json={"text": f"[IDX Witcher] {message}"}, timeout=10)
        except httpx.HTTPError:
            pass


def run_daily_pipeline(force: bool = False) -> None:
    provider = YahooProvider()
    if not force and not market_open_today(provider):
        log.info("Pasar tutup atau data belum terbit; pipeline dilewati")
        return
    steps = [
        ("prices", lambda: ingest_prices.run(provider)),
        ("indicators", lambda: compute_indicators.run()),
        ("fundamentals", lambda: ingest_fundamentals.run(provider)),
        ("rules", lambda: run_rules.run()),
    ]
    for name, fn in steps:
        result = fn()
        if result["status"] != "ok":
            alert(f"Pipeline berhenti di langkah '{name}': {result['error']}")
            return
    purge()
    log.info("Pipeline selesai")
