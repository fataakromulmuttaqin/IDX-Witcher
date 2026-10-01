# IDX Witcher

Platform riset saham Bursa Efek Indonesia (IDX) berbasis data end-of-day (EOD): peta pasar, screener fundamental, watchlist berbasis aturan, portofolio pribadi, dan daily feed.

> Disclaimer: alat riset dan edukasi, bukan saran investasi.

## Struktur Repo

```text
idx-witcher/
├── backend/          # Python 3.12: FastAPI, worker, ETL pipeline
├── frontend/         # React 18 + Vite + TypeScript
├── docs/             # PRD dan metodologi
├── docker-compose.yml
└── Makefile
```

## Setup Lokal

```bash
# 1. Environment
cp .env.example .env
# edit .env sesuai kebutuhan

# 2. Jalankan database dan Redis
docker compose up -d db redis

# 3. Setup backend
cd backend
python3.12 -m venv .venv
# .venv\Scripts\activate pada Windows
pip install -e ".[dev]"
alembic upgrade head
python -m worker.cli seed

# 4. Backfill data historis (opsional, memakan waktu)
python -m worker.cli backfill --start 2021-01-01

# 5. Jalankan API dan worker (di terminal terpisah atau via docker compose)
uvicorn app.main:app --reload
python -m worker.main

# 6. Setup frontend
cd ../frontend
npm install
npm run dev
```

## Perintah Berguna

```bash
make up        # docker compose up -d --build
make seed      # seed sectors dan companies
make backfill  # isi riwayat harga
make test      # pytest backend
make lint      # ruff backend
```

## Arsitektur

- **Pre-compute:** worker menghitung indikator dan aturan sekali per hari setelah penutupan bursa.
- **Read-only API:** FastAPI hanya membaca tabel hasil hitung.
- **Sumber data MVP:** Yahoo Finance via `yfinance` dengan antarmuka `DataProvider` agar mudah diganti.
- **Frontend:** React SPA, state lokal untuk portofolio.

## Dokumentasi

- `docs/PRD.md` — Product Requirements Document lengkap.
- `docs/METHODOLOGY.md` — Metodologi dan disclaimer untuk halaman Start Here.
