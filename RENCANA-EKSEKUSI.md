# Rencana Eksekusi IDX Witcher

**Status:** Draft untuk dimulai  
**Pilihan awal yang sudah diputuskan:**
- Lokasi project: folder baru `IDX Witcher/`
- Backend: **FastAPI + PostgreSQL + DuckDB**
- Auth & billing: **skip di awal** (fokus data + AI)
- Deployment target: **Vercel (frontend) + Railway/Fly.io (backend)**

---

## Pendekatan Umum

Kami membangun IDX Witcher dengan pola **"monorepo modular"**:

```
IDX Witcher/
├── apps/
│   ├── web/                 # Frontend Next.js/React 19 + Tailwind
│   └── api/                 # FastAPI backend
├── packages/
│   ├── shared/              # Skema, tipe, konstanta
│   └── ai/                  # Model NeuralAlpha (PyTorch inference)
├── infra/
│   ├── docker-compose.yml   # Dev local
│   └── fly.toml / railway.json
├── data/
│   └── parquet/             # Time-series lokal (gitignored)
└── README.md / docs/
```

**Prinsip kerja:**
1. **Phase 0:** Setup repo + dev environment + data pipeline jalan.
2. **Phase 1:** Backend FastAPI solid (data + screener + chart API).
3. **Phase 2:** Frontend web jalan (dashboard + screener + halaman saham).
4. **Phase 3:** Integrasi AI model NeuralAlpha (inference service + portfolio builder).
5. **Phase 4:** Polish, deployment, monitoring.

Tiap fase menghasilkan milestone yang **bisa didemo**.

---

## Fase 0 — Setup Fondasi & Dev Environment

**Tujuan:** repo bisa dijalankan di mesin developer, data pipeline berjalan, struktur modular siap.

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| P0-1 | Inisialisasi monorepo | `IDX Witcher/` dengan `apps/`, `packages/`, `infra/` | `README.md` menjelaskan cara setup |
| P0-2 | Setup `apps/api/` FastAPI skeleton | `/health`, `/docs`, struktur router, env config | `uv run uvicorn main:app` jalan |
| P0-3 | Setup `apps/web/` Next.js 15 + Tailwind 4 | Halaman root, layout, routing dasar | `pnpm dev` jalan di `localhost:3000` |
| P0-4 | Setup PostgreSQL & DuckDB via Docker Compose | `docker compose up` jalan | Service `db`, `duckdb`, `redis` reachable |
| P0-5 | Setup Alembic + tabel dasar | Skema `companies`, `prices`, `users` (stub) | Migration pertama berhasil |
| P0-6 | Setup lint, format, typecheck | Ruff, mypy, Prettier, husky | Pre-commit hook aktif |
| P0-7 | Setup env file template | `.env.example` | Semua secret di luar repo |
| P0-8 | Dokumentasi API awal | `docs/API.md` sederhana | Endpoint health & price tercatat |

**Milestone:** repo clean, bisa dijalankan, API health check OK.

---

## Fase 1 — Data Pipeline & Backend API (6 minggu)

**Tujuan:** backend dapat mengumpulkan, validasi, dan menyajikan data pasar IDX/BEI.

### Sprint 1.1 — Ingestion Layer

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| D1-1 | Clone & audit `idx-bei` scrapers | Module `packages/idx_scrapers/` | Beberapa scraper utama jalan standalone |
| D1-2 | Port scraper ke `apps/api/services/idx/` | Service `idx_client.py` | Test unit scraper > 70% |
| D1-3 | Implement Yahoo Finance fallback | `services/yahoo.py` | Fallback aktif bila IDX gagal |
| D1-4 | Implementasi validator & provenance | Middleware `source` & `quality_flag` | Setiap record menyimpan sumber data |
| D1-5 | Scheduler harian (APScheduler/Celery Beat) | Job `daily_ingest` | Data ter-update otomatis tiap hari |
| D1-6 | Backfill command (CLI + API) | Endpoint `/admin/backfill` | Bisa backfill rentang tanggal |

### Sprint 1.2 — Storage & Query

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| D2-1 | Skema PostgreSQL lengkap | Migration: prices, companies, fundamentals, actions, brokers, indices | Tabel tersedia |
| D2-2 | Parquet time-series layer | Script ekspor Parquet harian | File parquet dihasilkan per partition |
| D2-3 | DuckDB query layer | `services/query.py` read-only | Query OHLCV < 1s untuk 1 ticker |
| D2-4 | Cache Redis | Redis caching untuk hot data | Cache hit > 60% untuk endpoint populer |
| D2-5 | Health monitoring pipeline | `/health/data` status ingest | Tampilkan last ingest & gap |

### Sprint 1.3 — REST API Market Data

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| D3-1 | `/api/prices/{ticker}` | Endpoint OHLCV + filter date range | Response JSON valid, paged |
| D3-2 | `/api/companies` & `/{ticker}` | List & detail perusahaan | Pagination, search, filter |
| D3-3 | `/api/market/summary` | Summary IHSG, sectors, top movers | Update harian otomatis |
| D3-4 | `/api/screen` | Screener multi-faktor endpoint | Filter via query params |
| D3-5 | `/api/foreign-flow` | Net foreign buy/sell per ticker | Periode custom |
| D3-6 | `/api/brokers` | Broker summary, CR1/CR3/CR5 | Per tanggal |
| D3-7 | `/api/corporate-actions` | Aksi korporasi | Filter ticker & type |
| D3-8 | OpenAPI docs & tests | Pytest untuk semua endpoint | Coverage > 80% |

**Milestone:** API data lengkap, bisa dihitung oleh Postman/frontend.

---

## Fase 2 — Frontend Web (6 minggu)

**Tujuan:** pengguna dapat melihat dashboard pasar, screener, dan chart saham.

### Sprint 2.1 — Design System & Layout

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| F2-1 | Setup shadcn/ui atau komponen sendiri | Component library: Button, Card, Table, Input, Select | Konsisten di seluruh app |
| F2-2 | Layout app (sidebar, header, footer) | `AppLayout.tsx` | Responsif mobile & desktop |
| F2-3 | Theme & tokens Tailwind | `globals.css` + tailwind config | Dark/light mode |
| F2-4 | Setup tanstack-query | `lib/api.ts` hooks | Fetching, caching, error handling |

### Sprint 2.2 — Dashboard & Market Overview

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| F2-5 | Halaman Beranda | `page.tsx` dengan ringkasan pasar | Tampil IHSG, foreign, sektor |
| F2-6 | Ticker list / watchlist | Komponen tabel saham | Sort, search, pagination |
| F2-7 | Chart saham | TradingView Lightweight Charts v5 | OHLCV + EMA-20/50 |
| F2-8 | Halaman detail saham | `/stocks/[ticker]` | Chart, profil, fundamental, broker |

### Sprint 2.3 — Screener & Signals

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| F2-9 | Screener UI | `/screener` dengan filter multi-faktor | Apply filter, export CSV |
| F2-10 | Signals / Briefing harian | `/signals` | Tampil 8-screen summary |
| F2-11 | Bandarmology UI | `/bandarmology` | CR chart, stealth scan |
| F2-12 | Dividend radar | `/dividends` | Yield, trap risk |

**Milestone:** Website usable untuk analis data; no AI yet.

---

## Fase 3 — AI Engine & Portfolio Builder (6 minggu)

**Tujuan:** integrasi model NeuralAlpha, menghasilkan rekomendasi portofolio.

### Sprint 3.1 — AI Service

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| AI3-1 | Port model NeuralAlpha ke `packages/ai/` | Module `inference.py` | Bisa load weights & predict |
| AI3-2 | Feature pipeline real-time | Build feature panel dari data pipeline | Output sama format dengan model |
| AI3-3 | Inference endpoint `/api/ai/predict` | FastAPI endpoint | < 30s untuk LQ45 |
| AI3-4 | Model versioning & artifact store | Simpan model di object storage atau path | Versioning tercatat |
| AI3-5 | Baseline benchmarks | Endpoint `/api/ai/benchmark` | IHSG, 1/N equal weight |

### Sprint 3.2 — Optimizer & Portfolio

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| AI3-6 | Mean-variance optimizer | `services/optimizer.py` | Hasil weight sesuai constraints IDX |
| AI3-7 | Profil risiko (konservatif/moderat/agresif) | Mapping target return & max weight | Input profil, output portofolio |
| AI3-8 | Backtest engine | `/api/portfolio/backtest` | Sharpe, drawdown, equity curve |
| AI3-9 | Explainability | `/api/portfolio/{id}/explain` | Feature importance per rekomendasi |

### Sprint 3.3 — Portfolio UI

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| F3-1 | Portfolio Builder wizard | `/portfolio/builder` | 3 langkah: profil → preview → save |
| F3-2 | Portfolio result page | Tampilan weight, metrik, chart | Responsif |
| F3-3 | Portfolio tracker | `/portfolio/tracker` | Pantau drift & P/L |
| F3-4 | Backtest lab UI | `/lab/backtest` | Parameter & equity curve interaktif |

**Milestone:** AI portfolio recommendation live & demoable.

---

## Fase 4 — Deployment, Polish & Monitoring (4 minggu)

**Tujuan:** produk online, aman, stabil, siap user.

| ID | Task | Deliverable | Acceptance Criteria |
|---|---|---|---|
| DEP-1 | Deploy backend ke Railway/Fly.io | Service live di URL | Health check OK |
| DEP-2 | Deploy frontend ke Vercel | Domain vercel.app | Routing & API calls work |
| DEP-3 | Setup CI/CD GitHub Actions | `.github/workflows/` | Test, lint, build otomatis |
| DEP-4 | Monitoring & logging | Sentry + Prometheus/Grafana | Alert error > threshold |
| DEP-5 | Rate limiting & CORS | Middleware limitasi | DDoS protection dasar |
| DEP-6 | Security hardening | Dependency scan, secret scan, HTTPS | Audit passing |
| DEP-7 | Documentation launch | `docs/README.md`, API docs | End-user guide |
| DEP-8 | Feedback loop | Tombol feedback, analytics | Data masuk |

**Milestone:** IDX Witcher live untuk beta tester.

---

## Total Estimasi Timeline

| Fase | Durasi | Output |
|---|---|---|
| Phase 0 | 1 minggu | Repo jalan |
| Phase 1 | 6 minggu | API data solid |
| Phase 2 | 6 minggu | Web dashboard |
| Phase 3 | 6 minggu | AI portfolio |
| Phase 4 | 4 minggu | Live production |
| **Total** | **~17–20 minggu** | MVP beta |

---

## Dependency Antar Fase

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4
                ▲                      ↑
                └────────── D2 ────────┘
                (storage/query harus jadi sebelum AI inference)
```

---

## Teknologi Detail per Layer

### Backend
- **FastAPI** 0.115+ + Pydantic v2
- **uv** package manager
- **SQLAlchemy 2.0** + Alembic
- **DuckDB** Python client + Parquet
- **APScheduler** atau **Celery Beat** untuk cron
- **Redis** untuk cache & task broker
- **pytest** + pytest-cov + httpx test client

### Frontend
- **Next.js 15** (App Router)
- **React 19** + **TypeScript**
- **Tailwind CSS 4** + shadcn/ui atau Radix
- **TanStack Query** (React Query) untuk data
- **TradingView Lightweight Charts**
- **Zustand** untuk state global

### AI
- **PyTorch** 2.14+
- **pandas**, **numpy**, **scikit-learn**
- Model weights (PT) NeuralAlpha
- ONNX export opsional untuk inference cepat

### DevOps
- **Docker & Docker Compose**
- **GitHub Actions**
- **Railway/Fly.io**
- **Vercel**
- **Sentry**

---

## Task yang Bisa Dikerjakan Sekarang (Week 1)

1. **Buat struktur folder monorepo.**
2. **Inisialisasi FastAPI backend** dengan `/health` endpoint.
3. **Inisialisasi Next.js frontend** dengan layout dasar.
4. **Setup Docker Compose** (Postgres + DuckDB-volume + Redis).
5. **Clone & audit `idx-bei`** — catat scraper mana yang masih aktif.
6. **Setup Git repo & push ke GitHub.**
7. **Definisikan kontrak API awal** (OpenAPI) untuk prices & companies.

---

## Checklist Persiapan Sebelum Mulai Coding

- [ ] Folder `IDX Witcher/` sudah dibuat
- [ ] Python 3.13+ & Node.js 20+ terinstall
- [ ] Docker Desktop terinstall & running
- [ ] Git repo initialized
- [ ] Akun Railway/Fly.io & Vercel siap
- [ ] Memilih nama domain (opsional)
- [ ] Memutuskan apakah menggunakan shadcn/ui atau komponen custom
- [ ] Memutuskan penyimpanan model AI (HuggingFace, S3, local)

---

## Catatan Penting

1. **Auth & billing diskip di awal**, tapi tetap siapkan tabel `users` stub supaya migrasi nanti mudah.
2. **Scraper IDX** harus dilakukan dengan sopan (rate-limit, retry, cache) dan disclaimer kuat.
3. **Yahoo Finance fallback** hanya untuk OHLCV; jangan pakai untuk foreign flow/fundamental.
4. **Model AI** jangan di-training ulang di server production kecuali infrastructure siap; fokus inference dulu.
5. **Lisensi MIT** memungkinkan komersialisasi, tapi tetap periksa dependency non-MIT.

---

## Next Step Recommendation

Saya sarankan mulai **Phase 0** sekarang:
1. Setup monorepo.
2. Skeleton FastAPI + Next.js.
3. Docker Compose dev environment.
4. `/health` endpoint connect ke frontend.

Kalau setuju, saya bisa langsung mulai generate kode untuk langkah-langkah tersebut.
