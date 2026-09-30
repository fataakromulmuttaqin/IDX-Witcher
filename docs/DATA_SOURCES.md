# Data Sources & Pipeline

IDX Witcher menggunakan multi-source data pipeline untuk memastikan ketersediaan dan kelengkapan data saham Indonesia.

## Priority Data Sources

| Priority | Source | Type | Use Case |
|---|---|---|---|
| 1 | **TradingView Scanner** | Unofficial API | Data real-time lengkap: harga, fundamental, teknikal |
| 2 | **Yahoo Finance** | Official-ish | OHLCV historis, fundamental fallback |
| 3 | **Investing.com** | Scraper | Quote & fundamental |
| 4 | **idx.co.id (BEI)** | Official | Data resmi, fallback |
| 5 | **Finnhub** | Official API | Hanya US, optional |

## TradingView Scanner

Endpoint: `POST https://scanner.tradingview.com/indonesia/scan`

Cakupan: **846 saham IDX** (per test terakhir)

Kolom tersedia:
- Harga: `close`, `change`, `volume`
- Fundamental: `market_cap_basic`, `price_earnings_ttm`, `earnings_per_share_basic_ttm`, `dividend_yield_recent`, `price_book_ratio`, `return_on_equity`, `debt_to_equity`, `gross_margin`, `net_margin`, `total_revenue`, `net_income`
- Teknikal: `RSI`, `RSI[1]`, `MACD.macd`, `EMA20`, `EMA50`, `EMA200`, `SMA20`, `SMA50`, `ATR`, `Volatility.D`
- Sektor: `sector`, `industry`

### Endpoints Backend

- `POST /ingestion/sync-tradingview` — sync semua perusahaan IDX ke DB
- `POST /ingestion/enrich-tradingview/{ticker}` — enrich satu perusahaan
- `GET /companies/{code}/details` — detail perusahaan dengan data TradingView, Investing.com, dan IDX

## Yahoo Finance

Primary source untuk OHLCV historis.

Endpoints:
- `POST /ingestion/ohlcv/{ticker}`
- `POST /ingestion/batch`
- `POST /ingestion/market-summary`

## Sync Pipeline

### Sync Perusahaan IDX

```bash
curl -X POST http://localhost:8000/ingestion/sync-tradingview
```

### Sync Harga Historis LQ45

```bash
curl -X POST "http://localhost:8000/ingestion/batch?tickers=BBCA,BBRI,TLKM,BMRI,ASII,INDF,UNVR,ICBP,ANTM,PTBA&period=5y"
```

### Populate Full Database

```bash
cd scripts
python populate_data.py
```

## Notes

- TradingView scanner tidak memerlukan API key.
- Rate limit TradingView tidak terdokumentasi; gunakan dengan sopan.
- Investing.com dan idx.co.id sering memblokir request otomatis karena WAF.
- Yahoo Finance adalah fallback paling reliable untuk OHLCV historis.
