# IDX Witcher

Platform riset dan optimasi portofolio saham Indonesia berbasis AI, menggabungkan infrastruktur data [idx-bei](https://github.com/nichsedge/idx-bei) dengan model AI [NeuralAlpha](https://github.com/raindragon14/NeuralAlpha).

## Struktur Repo

```
IDX Witcher/
├── apps/
│   ├── api/          # FastAPI backend
│   └── web/          # Next.js frontend
├── references/       # Referensi repo asli (tidak di-commit)
├── infra/            # Konfigurasi deployment
├── docker-compose.yml
└── README.md
```

## Prasyarat

- Python 3.11+
- Node.js 20+
- Docker Desktop (opsional)
- pip atau uv (Python package manager)

## Setup Development

### 1. Jalankan database (opsional — SQLite digunakan sebagai default)

Jika ingin PostgreSQL:

```bash
docker compose up -d
```

### 2. Setup backend

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
cp .env.example .env
uvicorn idxwitcher_api.main:app --reload
```

Backend berjalan di http://localhost:8000.

### 3. Setup frontend

```bash
cd apps/web
cp .env.local.example .env.local
npm install
npm run dev
```

Frontend berjalan di http://localhost:3000.

### 4. Seed data & ingestion

Setelah backend berjalan, jalankan dari terminal lain:

```bash
# Seed daftar perusahaan default (LQ45)
curl -X POST http://localhost:8000/ingestion/seed-companies

# Ingest harga saham dari Yahoo Finance (contoh BBCA)
curl -X POST "http://localhost:8000/ingestion/ohlcv/BBCA?period=1y"

# Ingest market summary IHSG
curl -X POST "http://localhost:8000/ingestion/market-summary?period=1y"

# Ingest batch beberapa saham
curl -X POST "http://localhost:8000/ingestion/batch?tickers=BBCA,BBRI,TLKM&period=1y"
```

## API Endpoints (Fase 1)

| Endpoint | Deskripsi |
|---|---|---|
| `GET /health` | Status API |
| `GET /companies` | List perusahaan |
| `GET /companies/{code}` | Detail perusahaan |
| `GET /prices/{ticker}` | OHLCV per ticker |
| `GET /prices/{ticker}/latest` | Harga terakhir |
| `GET /market/summary` | Ringkasan IHSG |
| `GET /market/top-movers` | Top volume |
| `GET /screen` | Screener sederhana |
| `POST /ingestion/seed-companies` | Seed LQ45 |
| `POST /ingestion/ohlcv/{ticker}` | Ingest Yahoo OHLCV |
| `POST /ingestion/batch` | Ingest batch |
| `POST /ingestion/market-summary` | Ingest IHSG summary |
| `GET /foreign-flow/{ticker}` | Placeholder (memerlukan data IDX) |
| `GET /brokers` | Placeholder (memerlukan data IDX) |
| `GET /corporate-actions/{ticker}` | Placeholder (memerlukan data IDX) |

Dokumen lengkap OpenAPI: http://localhost:8000/docs

## Verifikasi

- Health API: http://localhost:8000/health
- OpenAPI docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Dashboard: http://localhost:3000/dashboard

## Deployment

### Backend (Railway/Fly.io)

```bash
# Build image
docker build -t idx-witcher-api ./apps/api

# Push ke registry pilihan
```

### Frontend (Vercel)

```bash
cd apps/web
vercel --prod
```

## Catatan

- Proyek ini masih dalam tahap MVP (Phase 0–1).
- Auth & billing disengaja di-skip di awal; ditambahkan di fase berikutnya.
- Endpoint `/foreign-flow`, `/brokers`, `/corporate-actions` masih placeholder dan memerlukan integrasi scraper IDX lebih lanjut.
- Disclaimer: platform ini adalah alat riset, bukan nasihat investasi.

## Lisensi

MIT
