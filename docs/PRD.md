# IDX Witcher — Product Requirements Document

Sep 30, 2026 · @Fata Akromul Muttaqin

## 1. Ringkasan Eksekutif

IDX Witcher adalah platform riset saham Bursa Efek Indonesia (IDX) berbasis data penutupan harian yang mengubah ratusan saham menjadi peta pasar, daftar pantauan berbasis aturan, screener fundamental, pelacak portofolio, dan feed perubahan harian, dengan setiap aturan tercetak jelas di layar.

Dokumen ini adalah spesifikasi produk dan teknis untuk membangun IDX Witcher dari nol. Referensi pengamatan: [StockMap by Jatevo](https://stockmap.jatevo.ai/dashboard/), yang pada penutupan 30 September 2026 menampilkan 840 saham IDX dengan data Yahoo Finance. IDX Witcher adalah produk sendiri dengan nama, desain, aturan, dan kode sendiri.

### Masalah yang diselesaikan

- Data saham IDX tersebar di aplikasi sekuritas, situs bursa, dan spreadsheet pribadi, sehingga riset harian memakan waktu.
- Banyak screener bersifat kotak hitam: pengguna tidak tahu mengapa sebuah saham lolos atau gagal.
- Investor ritel sulit melihat cepat "apa yang berubah hari ini" dan siapa pemegang saham di atas 1%.

### Value proposition

1. **Transparan**: setiap daftar menampilkan rumusnya; setiap sel kosong menampilkan alasannya (bank, rugi, tidak ada data).
2. **Visual dulu**: satu layar peta pasar menunjukkan seluruh bursa berdasarkan kapitalisasi pasar dan pergerakan harga.
3. **Cepat**: semua hasil dihitung sekali setelah penutupan pasar dan disajikan dari tabel siap-baca, bukan dihitung saat pengguna membuka halaman.
4. **Ramah ritel**: portofolio tersimpan di peramban tanpa wajib mendaftar; fitur akun bersifat opsional.

### Prinsip produk

- **End-of-day (EOD) first**: data diperbarui sekali sehari setelah penutupan bursa. Bukan aplikasi trading real-time.
- **Riset, bukan rekomendasi**: seluruh layar menampilkan disclaimer bahwa hasil adalah filter mekanis untuk edukasi, bukan saran membeli atau menjual.
- **Dapat diaudit**: setiap angka dapat ditelusuri ke sumber dan waktu pembaruannya.

### Modul produk sekilas

| Modul | Fungsi | Sumber data utama |
| --- | --- | --- |
| Explore (Market Map) | Treemap seluruh saham per sektor, ukuran = market cap, warna = perubahan harga | Harga harian, jumlah saham beredar |
| Watchlist | Daftar otomatis: Leading Stocks, Leading Sectors, Focus List, Setups | Indikator teknikal hasil hitung |
| 1% Screener | Pemegang saham di atas 1%, float, perubahan kepemilikan, konglomerasi | Berkas kepemilikan bulanan IDX/KSEI |
| Screener | Saham dalam 14 menu fundamental dan 17 screen berbasis aturan | Fundamental Yahoo, laporan keuangan |
| Portfolio | Nilai holding, untung/rugi, alokasi sektor | Harga penutupan terbaru |
| Daily Feed | Perubahan 5 sesi terakhir: high/low baru, breakdown tren, lonjakan volume | Indikator harian |
| Company Models | Model kuartalan 5 emiten terbesar tiap sektor dalam spreadsheet | Laporan keuangan emiten |
| Start Here | Penjelasan metodologi dan sumber angka | Konten statis |

## 2. Tujuan, Non-Tujuan, dan Metrik Sukses

MVP dianggap berhasil bila pengguna dapat melihat kondisi seluruh pasar dalam satu layar, menyaring saham dengan aturan yang terbaca, dan mendapat data segar setiap hari kerja bursa tanpa intervensi manual.

### Tujuan produk

1. Menyajikan data harian seluruh saham IDX aktif (target awal: 800+ emiten) dengan keterlambatan maksimal 60 menit setelah penutupan.
2. Menyediakan minimal 4 daftar pantauan dan 10 screen berbasis aturan pada MVP, masing-masing dengan rumus yang tampil di UI.
3. Memuat halaman utama (Explore) di bawah 2 detik pada koneksi 4G.
4. Menyediakan portofolio pribadi yang tersimpan di peramban tanpa login.

### Non-tujuan (di luar cakupan)

- Data real-time atau intraday, order book, dan eksekusi transaksi.
- Rekomendasi beli/jual, sinyal berbayar, atau manajemen dana.
- Mendukung bursa di luar IDX pada versi 1.
- Aplikasi native iOS/Android (cukup web responsif/PWA).

### Metrik sukses (KPI)

| Kategori | Metrik | Target MVP (90 hari) |
| --- | --- | --- |
| Keandalan data | Hari bursa dengan pembaruan berhasil sebelum 18:00 WIB | ≥ 98% |
| Kelengkapan | Saham aktif yang punya harga penutupan hari itu | ≥ 99% |
| Kualitas | Lolos sanity check otomatis tanpa koreksi manual | ≥ 97% baris |
| Performa | LCP halaman Explore (p75) | < 2,5 detik |
| Performa | Latensi API screener (p95) | < 400 ms |
| Adopsi | Pengguna aktif mingguan | 500 |
| Retensi | Pengguna yang kembali pada minggu ke-4 | ≥ 25% |
| Engagement | Rata-rata screener dibuka per sesi | ≥ 2 |

Target adopsi dan retensi adalah asumsi awal untuk proyek pribadi/komunitas; sesuaikan setelah ada data pemakaian nyata.

## 3. Target Pengguna dan User Journey

Pengguna utama adalah investor ritel Indonesia yang sudah memakai aplikasi sekuritas tetapi butuh alat riset yang lebih cepat dan transparan.

### Persona

| Persona | Profil | Kebutuhan utama | Fitur kunci |
| --- | --- | --- | --- |
| Rina, investor pemula | 24 tahun, karyawan, portofolio di bawah Rp50 juta | Memahami pasar tanpa istilah rumit, menghindari saham tidak likuid | Market Map, Start Here, filter likuiditas |
| Bagas, swing trader | 33 tahun, trading paruh waktu | Menemukan saham tren naik dan setup breakout tiap sore | Watchlist (Leading, Setups), Daily Feed |
| Dewi, investor nilai | 41 tahun, fokus dividen dan valuasi | Menyaring saham murah berkualitas dan memodelkan kinerja | Screener fundamental, Company Models, dividen |
| Anton, pemerhati kepemilikan | 38 tahun, mengikuti pergerakan pemegang besar | Melihat siapa pemegang di atas 1% dan perubahannya | 1% Screener |

### User journey utama

**Journey A: pemindaian sore hari (Bagas)**

1. Membuka Explore, melihat peta "Today" dan sektor yang memimpin.
2. Membuka Watchlist Setups, membaca aturan di bagian atas daftar.
3. Mengklik saham untuk melihat detail (grafik, indikator, fundamental ringkas).
4. Menambahkan saham ke Portfolio atau pantauan pribadi.
5. Membuka Daily Feed untuk memastikan tidak ada lonjakan volume atau breakdown yang terlewat.

**Journey B: riset valuasi (Dewi)**

1. Membuka Screener, memilih menu Valuation, mengatur filter market cap ≥ Rp10T dan nilai transaksi harian ≥ Rp10B.
2. Mengurutkan berdasarkan skor persentil, membaca alasan sel abu-abu (bank, rugi, tidak ada data).
3. Membuka Company Models emiten pilihan, mengubah asumsi hijau, dan melihat perubahan proyeksi.

**Journey C: pelacakan pemegang saham (Anton)**

1. Membuka 1% Screener, mencari nama investor atau kode saham.
2. Membuka tab Changes untuk melihat pemegang yang menambah atau mengurangi porsi bulan ini.
3. Membuka tab Conglomerates untuk melihat seluruh kepemilikan satu grup.

## 4. Ruang Lingkup dan Prioritas

MVP mencakup enam fitur inti yang bisa dibangun dalam sekitar 8 minggu oleh satu developer full-stack; Company Models, akun pengguna, dan data kepemilikan menyusul di fase berikutnya.

| Fitur | Prioritas | Fase | Catatan |
| --- | --- | --- | --- |
| Pipeline harga harian + database | Must | MVP | Fondasi semua fitur |
| Explore: Market Map | Must | MVP | Treemap + periode Today/1M/YTD/1Y |
| Screener fundamental | Must | MVP | 14 menu, sortir, filter market cap dan nilai transaksi |
| Watchlist berbasis aturan | Must | MVP | Leading Stocks, Leading Sectors, Focus List, Setups |
| Daily Feed | Should | MVP | 5 sesi terakhir |
| Portfolio (lokal di peramban) | Should | MVP | Tanpa login |
| Halaman Start Here | Should | MVP | Metodologi dan disclaimer |
| Detail saham (grafik + ringkasan) | Should | MVP | Panel samping dari peta/tabel |
| 1% Screener | Could | Fase 2 | Butuh impor berkas kepemilikan bulanan |
| Company Models (spreadsheet) | Could | Fase 2 | Ekspor xlsx dulu, editor langsung belakangan |
| Akun pengguna + sinkron portofolio | Could | Fase 2 | Email + kata sandi atau Google OAuth |
| Alert email/Telegram | Could | Fase 3 | Notifikasi Daily Feed untuk watchlist pribadi |
| Backtest sederhana aturan watchlist | Won't (sekarang) | Fase 3+ | Perlu data historis bersih dan penanganan corporate action |
| Data real-time | Won't | - | Di luar visi EOD |

### Definisi selesai MVP

- Pipeline berjalan otomatis setiap hari bursa dan mencatat status di tabel `ingest_runs`.
- Semua halaman MVP dapat dibuka tanpa login dan berfungsi di layar 375 px.
- Setiap daftar dan screen menampilkan aturan dalam bahasa manusia serta ekspresi teknisnya.
- Disclaimer "bukan saran investasi" tampil di footer setiap halaman.

## 5. Spesifikasi Fitur Detail

Setiap modul ditulis dengan tujuan, perilaku, data yang dibutuhkan, dan kriteria penerimaan (acceptance criteria/AC) yang bisa diuji.

### 5.1 Explore: Market Map

**Tujuan**: memberi gambaran seluruh pasar dalam satu layar.

**Perilaku**

- Treemap: satu kotak per saham, dikelompokkan per sektor IDX-IC. Ukuran = market cap, warna = perubahan harga pada periode terpilih.
- Toggle periode: Today (1 sesi), 1 month (21 sesi bursa), YTD (sejak sesi pertama tahun berjalan), 1 year (252 sesi).
- Saham kecil digabung menjadi satu kotak "Lainnya" per sektor agar peta terbaca (ambang: kumulatif 5% terbawah market cap sektor atau market cap di bawah Rp500 miliar, mana yang lebih besar).
- Klik kotak membuka panel detail: harga, perubahan, market cap, nilai transaksi 20 hari, PER, PBV, dan tautan ke halaman saham.
- Header menampilkan "Harga per \<tanggal penutupan>, \<jam pembaruan> WIB" dan sumber data.

**AC**: (1) semua saham dengan harga hari itu tampil; (2) skala warna simetris antara −5% dan +5% pada Today, dan otomatis lebih lebar untuk periode panjang; (3) render 800+ kotak tetap di atas 30 fps saat hover.

### 5.2 Watchlist berbasis aturan

**Tujuan**: daftar saham yang diperbarui setiap penutupan dan selalu mencetak aturannya.

| Daftar | Aturan ringkas | Maksud |
| --- | --- | --- |
| Leading Stocks | Tren naik jangka menengah + RS tinggi + likuid | Saham yang memimpin pasar |
| Leading Sectors | Sektor dengan median return 3 bulan tertinggi dan proporsi saham di atas SMA50 tinggi | Rotasi sektor |
| Focus List | Irisan Leading Stocks dan Leading Sectors, harga dekat puncak 52 minggu | Kandidat teratas untuk dipantau |
| Setups | Breakout volume, pullback ke SMA20 dalam tren naik, penyempitan volatilitas | Kandidat titik masuk teknikal |

Rumus lengkap ada di bagian 10.

**Perilaku**: tiap daftar punya slug (`/watchlist/leading-stocks`), kartu aturan di atas tabel, kolom Ticker, Nama, Sektor, Harga, 1D%, 1M%, RS, Jarak ke High 52W, dan tombol "Tambah ke pantauan pribadi".

**AC**: (1) daftar dihitung ulang tiap hari bursa; (2) jumlah anggota dan tanggal hitung tampil; (3) mengubah ekspresi aturan di konfigurasi tidak memerlukan perubahan kode frontend.

### 5.3 Screener fundamental

**Tujuan**: menyaring seluruh saham dengan menu fundamental dan screen berbasis aturan.

**Perilaku**

- 14 menu: Overview, Valuation, Profitability, Growth, Dividends, Balance Sheet, Cash Flow, Quality, Efficiency, Momentum, Technical, Liquidity, Size, Ownership. Tiap menu = kumpulan kolom siap tampil.
- 17 screen bernama aturan (mis. "Murah dan menguntungkan", "Dividen konsisten", "Utang rendah", "Pertumbuhan laba"), masing-masing dengan ekspresi filter.
- Filter global: sektor, market cap (Any, ≥ Rp1 T, ≥ Rp10 T, ≥ Rp50 T), nilai transaksi harian (Any, ≥ Rp1 M, ≥ Rp10 M, ≥ Rp50 M), jumlah baris (30/50/100/All), pencarian teks.
- Sortir dengan klik header kolom; skor = ringkasan persentil.
- Sel kosong menampilkan kata abu-abu berisi alasan: `bank` (rasio tidak berlaku bagi bank/asuransi/pembiayaan), `no data` (tidak ada laporan di sumber), `loss` (laba TTM negatif), `n/a` (tidak dilaporkan atau dibuang sanity check). Hover menampilkan penjelasan.
- Angka TTM (trailing twelve months); laporan berdenominasi USD dikonversi ke rupiah dengan kurs terkini.

**AC**: (1) sortir 800 baris di bawah 100 ms di sisi klien; (2) tidak ada sel kosong tanpa alasan; (3) ekspor CSV tersedia.

## 6. Sumber Data dan Strategi Akuisisi

MVP memakai Yahoo Finance lewat pustaka `yfinance` untuk harga dan fundamental, tetapi semua akses data dibungkus antarmuka `DataProvider` agar sumber bisa diganti ke penyedia berlisensi tanpa mengubah sisa sistem.

### Peta sumber data

| Data | Sumber MVP | Frekuensi | Catatan |
| --- | --- | --- | --- |
| Daftar emiten + sektor | Berkas daftar saham di situs IDX (impor CSV) + pemetaan manual `sector_map.csv` ke 11 sektor IDX-IC | Mingguan | Kode Yahoo = `KODE.JK` (mis. `BBCA.JK`) |
| Harga OHLCV harian | `yfinance` (`yf.download`) | Harian, setelah penutupan | Simpan `close` dan `adj_close` |
| Jumlah saham beredar, market cap | `yfinance` info / daftar IDX | Mingguan | Market cap dihitung sendiri: close × shares |
| Fundamental TTM | `yfinance` (info + laporan keuangan) | Mingguan, dan saat laporan baru terbit | Rasio dihitung sendiri dari laporan bila memungkinkan |
| Laporan keuangan kuartalan | `yfinance` (income, balance sheet, cash flow) | Mingguan | Cadangan: berkas XBRL/PDF dari IDX |
| Dividen dan stock split | `yfinance` (actions) | Harian | Dipakai untuk sinyal Dividend |
| Kurs USD/IDR | `yfinance` simbol `IDR=X` | Harian | Konversi laporan berdenominasi USD |
| Indeks IHSG | `yfinance` simbol `^JKSE` | Harian | Pembanding relative strength |
| Kepemilikan ≥1% | Berkas bulanan bursa/KSEI | Bulanan | Fase 2, impor CSV/XLSX |

### Risiko sumber dan mitigasinya

- `yfinance` adalah pustaka tidak resmi yang menarik data dari Yahoo. Yahoo dapat mengubah format atau membatasi akses sewaktu-waktu, dan ketentuan layanannya membatasi penggunaan komersial. Untuk proyek pribadi/komunitas ini dapat diterima; untuk produk komersial gunakan penyedia data berlisensi.
- Mitigasi teknis: antarmuka `DataProvider`, unduh dalam batch 50 ticker, jeda antar-batch, retry dengan backoff, dan simpan hasil mentah agar pemrosesan ulang tidak memanggil ulang sumber.
- Data saham IDX di Yahoo dapat memiliki lubang (hari tanpa data, volume 0, harga basi untuk saham suspensi). Pipeline wajib memakai sanity check berikut.

### Aturan sanity check (kualitas data)

1. Harga open/high/low/close harus > 0 dan `low ≤ close ≤ high`; baris yang melanggar ditandai `is_suspect` dan dikecualikan dari indikator.
2. Perubahan harian absolut > 35% tanpa aksi korporasi dianggap mencurigakan (batas auto-reject IDX bervariasi; nilai ini sengaja longgar).
3. Saham dengan volume 0 selama 5 sesi berturut-turut ditandai `illiquid` atau `suspended`.
4. Market cap hasil hitung dibandingkan dengan nilai sumber; selisih > 20% memicu peringatan.
5. Rasio ekstrem dibuang ke `n/a`: PER > 1.000 atau < 0, PBV > 100, ROE > 500%.
6. Setiap run mencatat jumlah baris, jumlah saham yang gagal, dan durasi di `ingest_runs`; run gagal > 5% ticker memicu alert.

### Aturan khusus pasar Indonesia

- 1 lot = 100 lembar; semua hitung portofolio memakai lembar = lot × 100.
- Kalender bursa: hari libur IDX tidak ada data; jangan isi nilai sintetis, cukup lewati.
- Emiten keuangan (bank, asuransi, pembiayaan) memakai logika rasio berbeda: tandai `is_financial = true` dan tampilkan `bank` pada rasio yang tidak berlaku (mis. Debt/Equity, EV/EBITDA, current ratio).
- Zona waktu: seluruh penjadwalan memakai `Asia/Jakarta` (WIB, UTC+7).

## 7. Arsitektur Sistem

Arsitektur memisahkan jalur tulis dan jalur baca: worker menghitung semua hasil sekali setelah penutupan bursa, dan API hanya membaca tabel yang sudah siap.

&#91;embedded content: arsitektur · 6 lapisan, satu arah\]

Worker adalah satu-satunya penulis ke PostgreSQL; API dan web tidak pernah memanggil Yahoo Finance secara langsung.

### Tech stack

| Lapisan | Pilihan | Alasan |
| --- | --- | --- |
| Bahasa backend | Python 3.12 | Ekosistem data (pandas, yfinance) paling lengkap |
| API | FastAPI + Pydantic v2 | Cepat, skema otomatis, dokumentasi OpenAPI gratis |
| ORM dan migrasi | SQLAlchemy 2 + Alembic | Skema versi-terkontrol |
| Pengolahan data | pandas | Rolling window dan groupby untuk indikator |
| Penjadwal | APScheduler di container worker | Sederhana; alternatif: cron atau GitHub Actions terjadwal |
| Database | PostgreSQL 16 | Relasional, JSONB untuk alasan sel kosong |
| Cache | Redis 7 | Cache respons dan rate limit |
| Frontend | React 18 + Vite + TypeScript | Build cepat |
| Styling | Tailwind CSS | Desain konsisten, tema gelap mudah |
| Data fetching | TanStack Query | Cache sisi klien dan status loading |
| Tabel | TanStack Table | Sortir, filter, virtualisasi |
| Grafik | Apache ECharts (treemap) + lightweight-charts (harga) | Treemap matang; grafik harga ringan |
| State | Zustand | Portofolio dan filter di peramban |
| Kontainer | Docker Compose | Lingkungan lokal dan produksi sama |
| CI | GitHub Actions | Tes, lint, build otomatis |

Catatan: saran awal saya di chat memakai create-react-app; diganti Vite karena CRA tidak lagi dikembangkan aktif.

### Alur data harian

1. Penjadwal memicu job pada pukul 17:00 WIB setiap hari kerja (hari libur bursa dilewati).
2. Provider mengunduh OHLCV dalam batch dan menyimpan hasil mentah.
3. Validasi (bagian 6) menandai baris mencurigakan.
4. Upsert ke `prices_daily`.
5. Hitung indikator ke `indicators_daily` dan snapshot fundamental ke `fundamentals_snapshot`.
6. Jalankan aturan watchlist dan screen, tulis `watchlist_members` dan `signals`.
7. Catat hasil di `ingest_runs`, hapus cache Redis, lalu frontend membaca data terbaru.

### Keputusan arsitektur

- **Pre-compute, bukan hitung saat diminta**: indikator dan daftar dihitung sekali per hari sehingga API tetap cepat walau jumlah pengguna naik.
- **Monolit modular dalam satu monorepo**: satu repo berisi `backend`, `worker`, dan `frontend`; dua proses Python berbagi paket `core`. Tidak perlu microservice pada skala ini.
- **Screener disortir di klien**: API mengirim seluruh tabel screener satu kali (sekitar 800 baris, perkiraan ratusan KB setelah kompresi gzip) dan TanStack Table menyortir/memfilter di peramban, sehingga interaksi instan.

## 8. Desain Database

Database memakai PostgreSQL 16 dengan 15 tabel yang dikelompokkan menjadi referensi, data pasar, hasil hitung, kepemilikan, dan operasional; semua tabel besar berkunci gabungan (ticker, tanggal) agar upsert harian idempoten.

### Kelompok tabel

| Kelompok | Tabel | Isi |
| --- | --- | --- |
| Referensi | `sectors`, `companies` | Sektor IDX-IC dan daftar emiten |
| Data pasar | `prices_daily`, `corporate_actions`, `financial_statements` | Harga, dividen/split, laporan keuangan long-format |
| Hasil hitung | `indicators_daily`, `fundamentals_snapshot`, `watchlists`, `watchlist_members`, `signals` | Indikator, rasio, daftar, dan sinyal |
| Kepemilikan (Fase 2) | `holders`, `holder_groups`, `holdings` | Pemegang ≥1%, grup konglomerasi |
| Operasional | `ingest_runs`, `users` | Log job dan akun (Fase 2) |

### Skema SQL lengkap

```sql
-- 001_init.sql  (PostgreSQL 16)
CREATE TABLE sectors (
  id        SMALLINT PRIMARY KEY,
  code      TEXT NOT NULL UNIQUE,          -- mis. 'FIN'
  name      TEXT NOT NULL                  -- 'Financials'
);

CREATE TABLE companies (
  ticker            TEXT PRIMARY KEY,      -- 'BBCA'
  yahoo_symbol      TEXT NOT NULL UNIQUE,  -- 'BBCA.JK'
  name              TEXT NOT NULL,
  sector_id         SMALLINT REFERENCES sectors(id),
  subsector         TEXT,
  board             TEXT,                  -- Utama/Pengembangan/Akselerasi
  listing_date      DATE,
  shares_outstanding BIGINT,
  is_financial      BOOLEAN NOT NULL DEFAULT FALSE,
  is_active         BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE prices_daily (
  ticker       TEXT NOT NULL REFERENCES companies(ticker),
  trade_date   DATE NOT NULL,
  open         NUMERIC(18,4),
  high         NUMERIC(18,4),
  low          NUMERIC(18,4),
  close        NUMERIC(18,4) NOT NULL,
  adj_close    NUMERIC(18,4),
  volume       BIGINT,
  value_traded NUMERIC(24,2),              -- aproksimasi: close * volume
  is_suspect   BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (ticker, trade_date)
);
CREATE INDEX ix_prices_date ON prices_daily (trade_date);

CREATE TABLE corporate_actions (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  action_date DATE NOT NULL,
  kind        TEXT NOT NULL CHECK (kind IN ('dividend','split')),
  value       NUMERIC(18,6) NOT NULL,      -- Rp/lembar atau rasio split
  PRIMARY KEY (ticker, action_date, kind)
);

CREATE TABLE financial_statements (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  period_end  DATE NOT NULL,
  period_type TEXT NOT NULL CHECK (period_type IN ('Q','FY')),
  statement   TEXT NOT NULL CHECK (statement IN ('IS','BS','CF')),
  item        TEXT NOT NULL,               -- 'TotalRevenue', 'NetIncome', ...
  value       NUMERIC(28,2),
  currency    TEXT NOT NULL DEFAULT 'IDR',
  source      TEXT NOT NULL DEFAULT 'yfinance',
  PRIMARY KEY (ticker, period_end, period_type, statement, item)
);

CREATE TABLE indicators_daily (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  trade_date  DATE NOT NULL,
  ret_1d      REAL, ret_1m REAL, ret_3m REAL, ret_ytd REAL, ret_1y REAL,
  sma20 REAL, sma50 REAL, sma150 REAL, sma200 REAL,
  hi_52w REAL, lo_52w REAL,
  vol_avg20   DOUBLE PRECISION,
  value_avg20 DOUBLE PRECISION,
  atr14       REAL,
  rs_rating   SMALLINT,                    -- 1..99 persentil kekuatan relatif
  PRIMARY KEY (ticker, trade_date)
);

CREATE TABLE fundamentals_snapshot (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  as_of       DATE NOT NULL,
  market_cap  NUMERIC(28,2),
  pe_ttm REAL, pb REAL, ps REAL, ev_ebitda REAL,
  roe REAL, roa REAL, gross_margin REAL, op_margin REAL, net_margin REAL,
  debt_equity REAL, current_ratio REAL,
  div_yield REAL, payout REAL,
  revenue_ttm NUMERIC(28,2), net_income_ttm NUMERIC(28,2), fcf_ttm NUMERIC(28,2),
  rev_growth_yoy REAL, eps_growth_yoy REAL,
  na_reason   JSONB NOT NULL DEFAULT '{}'::jsonb, -- {"pe_ttm":"loss","debt_equity":"bank"}
  PRIMARY KEY (ticker, as_of)
);

CREATE TABLE watchlists (
  slug        TEXT PRIMARY KEY,            -- 'leading-stocks'
  name        TEXT NOT NULL,
  description TEXT NOT NULL,               -- aturan dalam bahasa manusia
  rule_expr   TEXT NOT NULL,               -- ekspresi pandas.query
  sort_order  SMALLINT NOT NULL DEFAULT 0
);
CREATE TABLE watchlist_members (
  slug        TEXT NOT NULL REFERENCES watchlists(slug),
  trade_date  DATE NOT NULL,
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  rank        INTEGER,
  PRIMARY KEY (slug, trade_date, ticker)
);

CREATE TABLE signals (
  id          BIGSERIAL PRIMARY KEY,
  trade_date  DATE NOT NULL,
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  kind        TEXT NOT NULL,               -- new_high, volume_surge, ...
  detail      JSONB NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (trade_date, ticker, kind)
);
CREATE INDEX ix_signals_date ON signals (trade_date DESC);

-- Fase 2: kepemilikan
CREATE TABLE holder_groups (id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE holders (
  id              SERIAL PRIMARY KEY,
  name            TEXT NOT NULL,
  name_normalized TEXT NOT NULL UNIQUE,
  kind            TEXT,                    -- individual/corporate/fund/government
  group_id        INTEGER REFERENCES holder_groups(id),
  is_public_figure BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE holdings (
  ticker       TEXT NOT NULL REFERENCES companies(ticker),
  holder_id    INTEGER NOT NULL REFERENCES holders(id),
  report_month DATE NOT NULL,              -- tanggal 1 bulan laporan
  shares       BIGINT NOT NULL,
  pct          NUMERIC(7,4) NOT NULL,
  PRIMARY KEY (ticker, holder_id, report_month)
);

-- Operasional
CREATE TABLE ingest_runs (
  id          BIGSERIAL PRIMARY KEY,
  job         TEXT NOT NULL,               -- prices, fundamentals, indicators, rules
  started_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ,
  status      TEXT NOT NULL DEFAULT 'running',
  rows_written INTEGER,
  tickers_failed INTEGER,
  error       TEXT
);
CREATE TABLE users (   -- Fase 2
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  pw_hash    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Keputusan desain

- **Upsert idempoten**: semua job memakai `INSERT ... ON CONFLICT DO UPDATE` sehingga menjalankan ulang hari yang sama aman.
- **Indikator disimpan per hari** (bukan hanya terbaru) agar Daily Feed bisa membandingkan hari ini dengan kemarin tanpa menghitung ulang.
- **`na_reason` JSONB** menyimpan alasan sel kosong per kolom, dipakai UI untuk kata abu-abu.
- **Retensi**: simpan harga dan indikator minimal 5 tahun. Jika tabel melewati puluhan juta baris, partisi `prices_daily` per tahun atau pakai ekstensi TimescaleDB.
- **Uang**: nilai rupiah disimpan sebagai `NUMERIC`, rasio sebagai `REAL` (akurasi tampilan cukup).

## 9. Data Pipeline dan Job Terjadwal

Pipeline harian dijalankan berantai dalam satu fungsi `run_daily_pipeline()` yang dipicu 17:00 WIB pada hari kerja, sehingga tiap langkah hanya berjalan bila langkah sebelumnya berhasil.

### Daftar job

| Job | Pemicu (WIB) | Input | Output |
| --- | --- | --- | --- |
| `run_daily_pipeline` | Senin–Jumat 17:00 | Seluruh rantai di bawah | Data harian lengkap |
| 1. `check_market_open` | Langkah pertama rantai | Bar terakhir `^JKSE` | Lanjut bila tanggal bar = hari ini, selain itu berhenti tanpa error |
| 2. `ingest_prices` | Rantai | yfinance, 50 ticker per batch | `prices_daily` |
| 3. `ingest_actions` | Rantai | yfinance actions | `corporate_actions` |
| 4. `validate_prices` | Rantai | Baris baru | Kolom `is_suspect`, catatan di `ingest_runs` |
| 5. `compute_indicators` | Rantai | `prices_daily` | `indicators_daily` |
| 6. `run_rules` | Rantai | Indikator + fundamental | `watchlist_members`, `signals` |
| 7. `purge_cache` | Rantai | - | Hapus kunci Redis `iw:*` |
| `sync_companies` | Senin 06:00 | Berkas daftar saham IDX + `sector_map.csv` | `companies` |
| `ingest_fundamentals` | Sabtu 08:00 | yfinance info + laporan | `financial_statements` |
| `compute_fundamentals` | Setelah job di atas | Laporan + harga | `fundamentals_snapshot` |
| `import_holdings` | Bulanan, manual (Fase 2) | Berkas kepemilikan | `holders`, `holdings` |

### Aturan operasional

1. **Deteksi hari bursa**: pipeline tidak memakai kalender libur statis. Bila bar terakhir `^JKSE` bukan hari ini (libur atau data belum terbit), job berhenti dengan status `skipped`.
2. **Retry**: tiap batch mencoba hingga 3 kali dengan backoff eksponensial (2, 4, 8 detik) dan jeda acak antar-batch.
3. **Toleransi gagal**: ticker gagal dicatat di `ingest_runs.tickers_failed`. Bila > 5% ticker gagal, run berstatus `failed` dan alert dikirim.
4. **Rekonsiliasi**: setiap run juga mengunduh ulang 5 sesi terakhir untuk menangkap revisi data sumber (upsert menimpa nilai lama).
5. **Idempoten**: menjalankan ulang pipeline pada hari yang sama tidak menghasilkan duplikat.
6. **Backfill**: perintah `python -m worker.cli backfill --start 2021-01-01` mengisi riwayat awal, dalam potongan per tahun agar tidak terkena batas laju sumber.
7. **Alert**: kegagalan run dikirim ke Telegram bot atau webhook email; isi minimal: nama job, jumlah ticker gagal, pesan error pertama.

### Kebijakan fundamental

- Fundamental berubah lambat, jadi diperbarui mingguan dan tambahan ketika laporan baru terdeteksi (selisih `period_end` terbaru).
- TTM dihitung dari 4 kuartal terakhir bila ada; bila hanya laporan tahunan, pakai tahunan dan tandai `na_reason` bila data tidak cukup.
- Laporan berdenominasi USD dikonversi ke rupiah dengan kurs `IDR=X` pada `period_end`; simpan mata uang asli di `financial_statements.currency`.
- Emiten keuangan memakai `is_financial = true` dan rasio yang tidak berlaku diisi `bank` di `na_reason`.

## 10. Logika Bisnis dan Rumus

Semua aturan ditulis sebagai ekspresi `pandas.query` yang disimpan di konfigurasi, sehingga UI dapat menampilkan aturan yang sama persis dengan yang dijalankan. Ambang angka di bawah adalah nilai awal yang dapat disetel.

### 10.1 Indikator dasar

| Indikator | Definisi |
| --- | --- |
| `ret_n` | `close_t / close_(t-n) − 1`, dengan n = 1, 21 (1M), 63 (3M), 252 (1Y) sesi |
| `ret_ytd` | `close_t / close terakhir tahun sebelumnya − 1` |
| `sma_n` | Rata-rata `close` n sesi terakhir (n = 20, 50, 150, 200) |
| `hi_52w`, `lo_52w` | `close` tertinggi/terendah 252 sesi terakhir |
| `vol_avg20`, `value_avg20` | Rata-rata volume dan nilai transaksi 20 sesi |
| `atr14` | Rata-rata 14 sesi dari true range = `max(high−low, abs(high−close_prev), abs(low−close_prev))` |
| `value_traded` | `close × volume` (aproksimasi, karena sumber tidak memberi nilai transaksi) |

### 10.2 Relative Strength (RS Rating)

RS mengukur kekuatan harga relatif terhadap seluruh saham likuid. Skor mentah memberi bobot terbesar pada 3 bulan terakhir, lalu diubah menjadi peringkat persentil 1 sampai 99.

```latex
RS_{raw} = 0.4\, r_{63} + 0.2\, r_{126} + 0.2\, r_{189} + 0.2\, r_{252}
```

```latex
RS\ Rating = \mathrm{round}\left(99 \times \mathrm{percentile\ rank}(RS_{raw})\right)
```

Syarat: riwayat minimal 252 sesi; universe peringkat = saham dengan `value_avg20 ≥ Rp1 miliar` dan tidak `is_suspect`. Saham di luar syarat memiliki `rs_rating = NULL`.

### 10.3 Aturan watchlist

| Daftar | Ekspresi aturan | Bahasa manusia |
| --- | --- | --- |
| Leading Stocks | `close > sma50 and sma50 > sma150 and sma150 > sma200 and sma200 > sma200_20d_ago and rs_rating >= 70 and value_avg20 >= 1e9` | Tren naik bertingkat, SMA200 menanjak, kuat relatif, dan likuid |
| Leading Sectors | Skor sektor = 0,6 × persentil(median `ret_3m` anggota) + 0,4 × persentil(% anggota di atas SMA50); ambil 3 sektor teratas | Sektor yang memimpin rotasi |
| Focus List | `in_leading_stocks and sector_id in leading_sector_ids and close >= 0.90 * hi_52w` | Pemimpin di sektor pemimpin, dekat puncak |
| Setup: Breakout | `close >= hi_20d_prev and volume >= 1.5 * vol_avg20 and close > sma50` | Tembus puncak 20 sesi dengan volume |
| Setup: Pullback | `sma50 > sma200 and close > sma50 and 0.98 * sma20 <= close <= 1.02 * sma20` | Koreksi ke SMA20 dalam tren naik |
| Setup: Contraction | `atr14_pct <= 0.03 and atr14_pct < 0.8 * atr14_pct_20d_ago and close > sma50` | Volatilitas menyempit di atas SMA50 |

Kolom turunan (`sma200_20d_ago`, `hi_20d_prev`, `atr14_pct`, `atr14_pct_20d_ago`, `in_leading_stocks`, `leading_sector_ids`) dibentuk di memori oleh `run_rules` dan tidak disimpan di tabel.

### 10.4 17 screen fundamental

| # | Screen | Ekspresi |
| --- | --- | --- |
| 1 | Murah dan menguntungkan | `0 < pe_ttm <= 15 and roe >= 0.12` |
| 2 | Dividen konsisten | `div_yield >= 0.04 and 0 < payout <= 0.8 and net_income_ttm > 0` |
| 3 | Utang rendah | `debt_equity <= 0.5 and current_ratio >= 1.5` |
| 4 | Pertumbuhan laba | `eps_growth_yoy >= 0.2 and rev_growth_yoy >= 0.1` |
| 5 | Margin tinggi | `net_margin >= 0.15 and op_margin >= 0.2` |
| 6 | Di bawah nilai buku | `0 < pb < 1 and roe > 0` |
| 7 | Arus kas kuat | `fcf_ttm > 0 and fcf_ttm >= 0.8 * net_income_ttm` |
| 8 | Kualitas | `roe >= 0.15 and net_margin >= 0.1 and debt_equity <= 1` |
| 9 | Small cap likuid | `5e11 <= market_cap <= 5e12 and value_avg20 >= 1e9` |
| 10 | Big cap defensif | `market_cap >= 5e13 and div_yield >= 0.03` |
| 11 | Momentum kuat | `ret_3m >= 0.2 and close > sma50` |
| 12 | Dekat high 52 minggu | `close >= 0.95 * hi_52w` |
| 13 | Dekat low 52 minggu | `close <= 1.10 * lo_52w` |
| 14 | Terkoreksi di tren naik | `close > sma200 and ret_1m <= -0.10` |
| 15 | Likuiditas tinggi | `value_avg20 >= 5e10` |
| 16 | Pertumbuhan wajar | `0 < pe_ttm <= 25 and eps_growth_yoy >= 0.15` |
| 17 | Laba membaik | `net_income_ttm > 0 and eps_growth_yoy >= 0.5` |

Baris yang kolomnya `NULL` otomatis tidak lolos ekspresi (perilaku perbandingan pandas), sehingga emiten keuangan tidak muncul di screen berbasis rasio yang tidak berlaku bagi mereka.

### 10.5 Skor persentil screener

```latex
Score_i = 100 \times \frac{1}{|M|} \sum_{m \in M} \mathrm{pr}_m(x_{i,m})
```

`M` = metrik dalam satu menu yang tersedia untuk saham i; `pr` = peringkat persentil dalam universe (dibalik untuk metrik "lebih rendah lebih baik" seperti PER dan Debt/Equity). Skor dihitung hanya bila minimal 3 metrik tersedia; selain itu `NULL`.

### 10.6 Rumus portofolio

- Lembar = lot × 100
- Modal = lembar × harga rata-rata beli + biaya (bila diisi)
- Nilai pasar = lembar × harga penutupan terakhir
- Untung/rugi (Rp) = nilai pasar − modal; persen = untung/rugi ÷ modal
- Alokasi sektor = jumlah nilai pasar per sektor ÷ total nilai pasar

### 10.7 Definisi 14 menu screener

Semua menu otomatis diawali kolom `ticker`, `name`, `sector`, `market_cap`, dan `close`; tabel berikut hanya menyebut kolom tambahan dan metrik yang membentuk skor (bagian 10.5). Isi dengan format yang sama ke `rules/menus.yaml`.

| # | Menu | Kolom tambahan | Metrik skor |
| --- | --- | --- | --- |
| 1 | Overview | `ret_1d`, `pe_ttm`, `pb`, `div_yield`, `rs_rating` | Tinggi: `rs_rating`, `div_yield`. Rendah: `pe_ttm`, `pb` |
| 2 | Valuation | `pe_ttm`, `pb`, `ps`, `ev_ebitda`, `div_yield` | Tinggi: `div_yield`. Rendah: `pe_ttm`, `pb`, `ps`, `ev_ebitda` |
| 3 | Profitability | `roe`, `roa`, `gross_margin`, `op_margin`, `net_margin` | Tinggi: semua kolom |
| 4 | Growth | `rev_growth_yoy`, `eps_growth_yoy`, `revenue_ttm`, `net_income_ttm` | Tinggi: `rev_growth_yoy`, `eps_growth_yoy`, `net_income_ttm` |
| 5 | Dividends | `div_yield`, `payout`, `net_income_ttm`, `pe_ttm` | Tinggi: `div_yield`, `net_income_ttm`. Rendah: `pe_ttm` |
| 6 | Balance Sheet | `debt_equity`, `current_ratio`, `roe` | Tinggi: `current_ratio`, `roe`. Rendah: `debt_equity` |
| 7 | Cash Flow | `fcf_ttm`, `revenue_ttm`, `net_income_ttm` | Tinggi: semua kolom |
| 8 | Quality | `roe`, `roa`, `net_margin`, `debt_equity`, `current_ratio` | Tinggi: `roe`, `roa`, `net_margin`, `current_ratio`. Rendah: `debt_equity` |
| 9 | Efficiency | `roe`, `roa`, `op_margin` | Tinggi: semua kolom |
| 10 | Momentum | `ret_1m`, `ret_3m`, `ret_ytd`, `ret_1y`, `rs_rating` | Tinggi: semua kolom |
| 11 | Technical | `sma50`, `sma200`, `hi_52w`, `lo_52w`, `ret_1d` | Tanpa skor |
| 12 | Liquidity | `value_avg20`, `vol_avg20` | Tanpa skor |
| 13 | Size | `revenue_ttm`, `net_income_ttm` | Tanpa skor |
| 14 | Ownership | Float, pemegang ≥1%, perubahan kepemilikan | Fase 2 (menunggu data bagian 5.4) |

Menu tanpa skor diurutkan menurut `market_cap`. Menu dengan kurang dari 3 metrik tersedia untuk sebuah saham menampilkan skor `NULL` untuk saham itu.

## 11. Desain API

API bersifat baca-saja (kecuali fitur akun di Fase 2), berawalan `/api/v1`, memakai JSON `snake_case`, dan selalu membungkus hasil dengan tanggal data `as_of` agar UI dapat menampilkan "harga per tanggal".

### Endpoint

| Metode dan path | Fase | Fungsi |
| --- | --- | --- |
| `GET /health` | MVP | Status layanan dan database |
| `GET /meta` | MVP | `as_of`, status run terakhir, jumlah saham aktif |
| `GET /market-map?period=today\|1m\|ytd\|1y` | MVP | Data treemap: ticker, nama, sektor, market cap, perubahan |
| `GET /stocks/{ticker}` | MVP | Detail saham: harga, indikator, fundamental ringkas, sinyal |
| `GET /stocks/{ticker}/prices?range=1y` | MVP | Deret OHLCV untuk grafik |
| `GET /screener/menus` | MVP | Daftar 14 menu dan kolomnya |
| `GET /screener?menu=valuation&sector=&min_mcap=&min_value=&q=&limit=` | MVP | Tabel screener lengkap dengan `na_reason` |
| `GET /screens` dan `GET /screens/{slug}` | MVP | 17 screen: aturan dan anggota |
| `GET /watchlists` dan `GET /watchlists/{slug}?date=` | MVP | Daftar, aturan, dan anggota pada tanggal tertentu |
| `GET /feed?days=5&kind=&sector=` | MVP | Sinyal Daily Feed |
| `POST /portfolio/quote` | MVP | Body `{"tickers":["BBCA","TLKM"]}` mengembalikan harga terakhir; tidak menyimpan apa pun |
| `GET /holders/search?q=` | Fase 2 | Cari ticker atau investor |
| `GET /stocks/{ticker}/holders` | Fase 2 | Pemegang ≥1% saham tersebut |
| `GET /holdings/changes?month=` | Fase 2 | Perubahan kepemilikan |
| `GET /models/{ticker}.xlsx` | Fase 2 | Unduh model keuangan |
| `POST /auth/register`, `POST /auth/login`, `GET/PUT /me/portfolio` | Fase 2 | Akun dan sinkron portofolio |

### Contoh respons

`GET /api/v1/market-map?period=today`

Angka pada kedua contoh respons di bawah adalah ilustrasi, bukan data pasar.

```json
{
  "as_of": "2026-09-30",
  "period": "today",
  "data": [
    {"ticker": "BBCA", "name": "Bank Central Asia", "sector": "Financials",
     "market_cap": 1150000000000000, "change_pct": 0.0123},
    {"ticker": "TLKM", "name": "Telkom Indonesia", "sector": "Infrastructures",
     "market_cap": 310000000000000, "change_pct": -0.0081}
  ]
}
```

`GET /api/v1/screener?menu=valuation&min_mcap=1e12&limit=2` (angka ilustrasi)

```json
{
  "as_of": "2026-09-30",
  "menu": "valuation",
  "columns": ["ticker", "pe_ttm", "pb", "ps", "ev_ebitda", "score"],
  "data": [
    {"ticker": "XXXX", "pe_ttm": 9.8, "pb": 1.2, "ps": 1.5, "ev_ebitda": 6.1, "score": 74,
     "na_reason": {}},
    {"ticker": "YYYY", "pe_ttm": null, "pb": 2.1, "ps": 3.0, "ev_ebitda": null, "score": null,
     "na_reason": {"pe_ttm": "loss", "ev_ebitda": "bank"}}
  ]
}
```

### Konvensi

- **Angka mentah**: API tidak memformat angka (tanpa "Rp" atau "T"); pemformatan dilakukan di frontend. Persentase sebagai desimal (0,0123 = 1,23%).
- **Tanggal**: ISO 8601 (`YYYY-MM-DD`); stempel waktu dalam UTC dengan sufiks `Z`.
- **Error**: bentuk seragam `{"error": {"code": "not_found", "message": "Ticker ZZZZ tidak ditemukan"}}` dengan kode HTTP 400, 404, 422, 429, atau 500.
- **Versi**: perubahan yang merusak kompatibilitas menaikkan prefiks ke `/api/v2`.

### Caching dan batas laju

1. Respons baca di-cache di Redis dengan kunci `iw:<path>:<query-terurut>`; dihapus oleh `purge_cache` setiap akhir pipeline, dengan TTL pengaman 6 jam.
2. Header `Cache-Control: public, max-age=300` dan `ETag` agar CDN/peramban dapat memvalidasi ulang.
3. Batas laju awal 60 permintaan per menit per IP (middleware berbasis Redis); endpoint `/screener` dan `/market-map` dikecualikan dari penalti ketika dilayani dari cache.
4. CORS hanya mengizinkan domain frontend produksi dan `localhost` saat pengembangan.

## 12. Desain Frontend dan UX

Frontend adalah single-page app React yang visual-first: halaman Explore (peta pasar) menjadi beranda, dan semua tabel memakai pola yang sama (filter di atas, kartu aturan, tabel dengan sortir).

### Peta halaman

| Rute | Halaman | Fase |
| --- | --- | --- |
| `/` | Explore: Market Map + panel detail | MVP |
| `/watchlist/:slug` | Daftar pantauan dengan kartu aturan | MVP |
| `/screener/:menu` | Screener 14 menu | MVP |
| `/screens/:slug` | Screen berbasis aturan | MVP |
| `/feed` | Daily Feed 5 sesi terakhir | MVP |
| `/portfolio` | Portofolio lokal | MVP |
| `/stock/:ticker` | Detail saham | MVP |
| `/start` | Start Here: metodologi dan disclaimer | MVP |
| `/1pct` | 1% Screener (7 tab) | Fase 2 |
| `/models/:ticker` | Company Models | Fase 2 |

### Komponen utama

1. **AppShell**: header (logo IDX Witcher, pencarian ticker, toggle tema), navigasi samping/bawah (mobile), footer berisi disclaimer dan `as_of`.
2. **MarketMap**: treemap ECharts; data dari `/market-map`; toggle periode; klik membuka `StockPanel`.
3. **StockPanel**: panel geser berisi harga, perubahan, market cap, PER, PBV, dan tautan ke `/stock/:ticker`.
4. **RuleCard**: menampilkan nama daftar, aturan dalam bahasa manusia, ekspresi teknis (dapat dilipat), jumlah anggota, dan tanggal hitung.
5. **DataTable**: TanStack Table dengan sortir, kolom tetap (ticker), virtualisasi di atas 200 baris, dan ekspor CSV.
6. **NaCell**: sel kosong dengan kata abu-abu (`bank`, `no data`, `loss`, `n/a`) dan tooltip penjelasan.
7. **FilterBar**: sektor, market cap, nilai transaksi, jumlah baris, pencarian teks; status filter tersimpan di URL (`?mcap=1e12&sector=FIN`).
8. **PortfolioForm + AllocationDonut**: input holding dan grafik alokasi.
9. **FeedList**: kartu sinyal dikelompokkan per tanggal dengan chip jenis sinyal.
10. **PriceChart**: lightweight-charts dengan overlay SMA20/50/200.

### Spesifikasi Market Map

- Hierarki: sektor sebagai induk, saham sebagai daun; ukuran daun = `market_cap`.
- Skala warna divergen merah–abu–hijau (hijau = naik, merah = turun, sesuai kebiasaan pasar Indonesia), netral pada 0%.
- Label kotak: ticker dan persen perubahan; kotak yang terlalu kecil hanya menampilkan ticker saat hover (tooltip).
- Gabungkan saham kecil menjadi "Lainnya" per sektor sesuai aturan 5.1.
- Aksesibilitas: tersedia tampilan alternatif berupa tabel terurut untuk pembaca layar dan pengguna yang menonaktifkan grafik.

### Desain visual

| Token | Terang | Gelap | Pemakaian |
| --- | --- | --- | --- |
| `--bg` | #F7F8FA | #0D1117 | Latar halaman |
| `--surface` | #FFFFFF | #161B22 | Kartu dan tabel |
| `--border` | #E3E6EB | #262D36 | Garis |
| `--text` | #141821 | #E6EAF0 | Teks utama |
| `--muted` | #6B7280 | #8B95A5 | Teks sekunder, sel `n/a` |
| `--up` | #16A34A | #22C55E | Naik |
| `--down` | #DC2626 | #F87171 | Turun |
| `--accent` | #2563EB | #60A5FA | Tautan, fokus, tombol utama |

Tipografi: Inter untuk UI dan JetBrains Mono untuk angka tabel (angka tabular agar kolom rata). Sudut 8 px, bayangan minimal, jarak kelipatan 4 px.

### Format angka dan bahasa

- Lokal `id-ID`: pemisah ribuan titik, desimal koma (1.234,56).
- Nilai rupiah disingkat: T (triliun), M (miliar), Jt (juta). Singkatan B (billion) tidak dipakai di UI.
- Bahasa UI: Indonesia; istilah pasar baku (market cap, PER, PBV) dipertahankan.

### Perilaku dan performa

1. **Status**: skeleton saat memuat, pesan kosong yang informatif, dan tombol coba lagi saat error.
2. **Data fetching**: TanStack Query dengan `staleTime` 5 menit; data dianggap segar sampai pipeline berikutnya.
3. **Responsif**: breakpoint 640, 1024, 1280 px; di ponsel treemap memakai tinggi 70% layar dan tabel dapat digeser horizontal dengan kolom ticker tetap.
4. **Bundel**: pecah kode per rute (lazy import); ECharts diimpor modular (hanya treemap, tooltip, dan renderer Canvas).
5. **PWA (opsional)**: manifest dan service worker untuk "Tambahkan ke layar utama".
6. **Aksesibilitas**: kontras minimal WCAG AA, navigasi keyboard pada tabel dan filter, warna tidak menjadi satu-satunya penanda naik/turun (tambahkan tanda + / −).

## 13. Struktur Code Base

Proyek berupa satu monorepo dengan dua bagian: `backend` (Python: API, worker, dan kode bersama) dan `frontend` (React). API dan worker berbagi paket `core` agar model database dan konfigurasi tidak terduplikasi.

### Pohon folder

```text
idx-witcher/
├── README.md
├── .env.example
├── .gitignore
├── Makefile
├── docker-compose.yml
├── .github/workflows/ci.yml
├── docs/
│   ├── PRD.md
│   └── METHODOLOGY.md              # isi halaman Start Here
├── backend/
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/0001_init.py
│   ├── core/                        # dipakai API dan worker
│   │   ├── config.py                # pengaturan dari environment
│   │   ├── db.py                    # engine dan session SQLAlchemy
│   │   ├── models.py                # tabel ORM
│   │   ├── cache.py                 # klien Redis
│   │   └── rules.py                 # memuat dan menjalankan aturan YAML
│   ├── providers/                   # akses data eksternal
│   │   ├── base.py                  # antarmuka DataProvider
│   │   ├── yahoo.py                 # implementasi yfinance
│   │   └── idx_files.py             # impor berkas IDX/KSEI (CSV/XLSX)
│   ├── worker/
│   │   ├── main.py                  # penjadwal APScheduler
│   │   ├── pipeline.py              # run_daily_pipeline()
│   │   ├── cli.py                   # backfill, run-once, seed
│   │   ├── quality.py               # sanity check dan laporan kualitas
│   │   ├── indicators.py            # hitung SMA, return, ATR, RS
│   │   ├── fundamentals.py          # rasio dan na_reason
│   │   └── jobs/
│   │       ├── sync_companies.py
│   │       ├── ingest_prices.py
│   │       ├── ingest_actions.py
│   │       ├── ingest_fundamentals.py
│   │       ├── compute_indicators.py
│   │       ├── run_rules.py
│   │       └── import_holdings.py   # Fase 2
│   ├── rules/                       # konfigurasi aturan (bukan kode)
│   │   ├── watchlists.yaml
│   │   ├── screens.yaml
│   │   └── menus.yaml               # 14 menu dan kolomnya
│   ├── data/
│   │   ├── sector_map.csv           # ticker ke sektor IDX-IC
│   │   └── companies_seed.csv
│   ├── app/                         # FastAPI
│   │   ├── main.py
│   │   ├── deps.py
│   │   ├── schemas.py               # model Pydantic
│   │   ├── errors.py
│   │   └── routers/
│   │       ├── meta.py
│   │       ├── market_map.py
│   │       ├── stocks.py
│   │       ├── screener.py
│   │       ├── watchlists.py
│   │       ├── feed.py
│   │       └── portfolio.py
│   └── tests/
│       ├── test_indicators.py
│       ├── test_rules.py
│       ├── test_quality.py
│       └── test_api.py
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── index.html
    ├── public/
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── routes.tsx
        ├── api/                     # client.ts, types.ts, hooks.ts
        ├── components/
        │   ├── layout/              # AppShell, Header, Footer
        │   ├── charts/              # MarketMap, PriceChart, AllocationDonut
        │   ├── table/               # DataTable, NaCell, FilterBar
        │   └── common/              # RuleCard, StockPanel, Disclaimer
        ├── pages/                   # Explore, Watchlist, Screener, Screens,
        │                            # Feed, Portfolio, Stock, Start
        ├── store/                   # portfolio.ts, filters.ts, theme.ts
        ├── lib/                     # format.ts, colors.ts
        └── styles/index.css
```

### Tanggung jawab folder

| Folder | Tanggung jawab | Aturan |
| --- | --- | --- |
| `backend/core` | Konfigurasi, koneksi DB, model ORM, cache | Tidak boleh mengimpor dari `app` atau `worker` |
| `backend/providers` | Semua akses ke sumber data luar | Hanya di sini kode memanggil yfinance atau membaca berkas |
| `backend/worker` | Job terjadwal dan perhitungan | Satu-satunya penulis ke tabel data pasar dan hasil hitung |
| `backend/rules` | Aturan watchlist, screen, dan menu dalam YAML | Mengubah aturan = mengubah YAML, tanpa deploy frontend |
| `backend/app` | API baca-saja | Tidak memanggil sumber eksternal |
| `frontend/src/api` | Klien HTTP bertipe dan hook TanStack Query | Satu-satunya tempat yang memanggil `fetch` |
| `frontend/src/store` | State klien (Zustand) | Portofolio dipersistenkan ke `localStorage` |
| `frontend/src/lib` | Fungsi murni (format angka, warna) | Mudah diuji unit |

### Konvensi

- Python: versi 3.12, `ruff` untuk lint dan format, `mypy` untuk tipe, `pytest` untuk tes.
- TypeScript: mode `strict`, ESLint + Prettier, Vitest untuk tes unit.
- Commit: Conventional Commits (`feat:`, `fix:`, `chore:`); cabang utama `main`, fitur di `feat/*`.
- Konfigurasi rahasia hanya lewat environment (`.env`, tidak di-commit).

## 14. Kode Inti Siap Pakai

Bagian ini berisi kode jalur kritis: dari setup repo, pengambilan harga, indikator, aturan, pipeline, API, sampai komponen React pertama. Semua file lain (router tambahan, halaman, job fundamental) mengikuti pola yang sama. Versi paket di bawah adalah batas minimum perkiraan; kunci versi dengan lockfile setelah instalasi pertama dan jalankan tes sebelum dipakai.

### 14.1 Setup repo dan fondasi backend

```bash
mkdir idx-witcher && cd idx-witcher && git init
mkdir -p backend/{core,providers,worker/jobs,rules,data,app/routers,tests} docs
touch backend/{core,providers,worker,worker/jobs,app,app/routers}/__init__.py
cd backend && python3.12 -m venv .venv && source .venv/bin/activate
# setelah pyproject.toml dibuat:
pip install -e ".[dev]"
cd .. && npm create vite@latest frontend -- --template react-ts
cd frontend && npm i @tanstack/react-query @tanstack/react-table react-router-dom zustand echarts lightweight-charts
npm i -D tailwindcss@3 postcss autoprefixer vitest && npx tailwindcss init -p
```

`backend/pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "idx-witcher"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115",
  "uvicorn[standard]>=0.30",
  "sqlalchemy>=2.0",
  "psycopg[binary]>=3.2",
  "alembic>=1.13",
  "pydantic>=2.8",
  "pydantic-settings>=2.4",
  "pandas>=2.2",
  "numpy>=1.26",
  "yfinance>=0.2.50",
  "apscheduler>=3.10,<4",
  "redis>=5.0",
  "pyyaml>=6.0",
  "httpx>=0.27",
  "openpyxl>=3.1",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov", "ruff", "mypy", "types-PyYAML"]

[tool.setuptools.packages.find]
include = ["core*", "providers*", "worker*", "app*"]

[tool.ruff]
line-length = 100
```

`backend/core/config.py`

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://iw:iw@localhost:5432/idxwitcher"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:5173"]  # env: JSON, mis. '["https://iw.example"]'
    timezone: str = "Asia/Jakarta"
    pipeline_hour: int = 17
    yahoo_batch_size: int = 50
    yahoo_batch_sleep: float = 1.5
    alert_webhook_url: str | None = None
    history_start: str = "2021-01-01"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

`backend/core/db.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=10)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def upsert(session, model, rows: list[dict], keys: list[str], chunk: int = 2000) -> int:
    """INSERT ... ON CONFLICT DO UPDATE, per potongan agar tidak melewati batas parameter."""
    if not rows:
        return 0
    cols = [c for c in rows[0].keys() if c not in keys]
    for i in range(0, len(rows), chunk):
        stmt = insert(model).values(rows[i : i + chunk])
        stmt = stmt.on_conflict_do_update(
            index_elements=keys, set_={c: stmt.excluded[c] for c in cols}
        )
        session.execute(stmt)
    return len(rows)
```

`backend/core/models.py` (tabel yang dipakai kode di bawah; sisanya mengikuti skema bagian 8)

```python
from datetime import date, datetime

from sqlalchemy import (BigInteger, Boolean, Date, DateTime, Float, ForeignKey, Integer,
                        Numeric, SmallInteger, String, Text, func)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


def _float():
    return mapped_column(Float, nullable=True)


class Sector(Base):
    __tablename__ = "sectors"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)


class Company(Base):
    __tablename__ = "companies"
    ticker: Mapped[str] = mapped_column(String, primary_key=True)
    yahoo_symbol: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"))
    shares_outstanding: Mapped[int | None] = mapped_column(BigInteger)
    is_financial: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PriceDaily(Base):
    __tablename__ = "prices_daily"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    open: Mapped[float | None] = mapped_column(Numeric(18, 4))
    high: Mapped[float | None] = mapped_column(Numeric(18, 4))
    low: Mapped[float | None] = mapped_column(Numeric(18, 4))
    close: Mapped[float] = mapped_column(Numeric(18, 4))
    adj_close: Mapped[float | None] = mapped_column(Numeric(18, 4))
    volume: Mapped[int | None] = mapped_column(BigInteger)
    value_traded: Mapped[float | None] = mapped_column(Numeric(24, 2))
    is_suspect: Mapped[bool] = mapped_column(Boolean, default=False)


class IndicatorDaily(Base):
    __tablename__ = "indicators_daily"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    ret_1d: Mapped[float | None] = _float()
    ret_1m: Mapped[float | None] = _float()
    ret_3m: Mapped[float | None] = _float()
    ret_ytd: Mapped[float | None] = _float()
    ret_1y: Mapped[float | None] = _float()
    sma20: Mapped[float | None] = _float()
    sma50: Mapped[float | None] = _float()
    sma150: Mapped[float | None] = _float()
    sma200: Mapped[float | None] = _float()
    hi_52w: Mapped[float | None] = _float()
    lo_52w: Mapped[float | None] = _float()
    vol_avg20: Mapped[float | None] = mapped_column(Float(53))
    value_avg20: Mapped[float | None] = mapped_column(Float(53))
    atr14: Mapped[float | None] = _float()
    rs_rating: Mapped[int | None] = mapped_column(SmallInteger)


class WatchlistMember(Base):
    __tablename__ = "watchlist_members"
    slug: Mapped[str] = mapped_column(String, primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    rank: Mapped[int | None] = mapped_column(Integer)


class Signal(Base):
    __tablename__ = "signals"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    trade_date: Mapped[date] = mapped_column(Date)
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"))
    kind: Mapped[str] = mapped_column(String)
    detail: Mapped[dict] = mapped_column(JSONB, default=dict)


class IngestRun(Base):
    __tablename__ = "ingest_runs"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    job: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String, default="running")
    rows_written: Mapped[int | None] = mapped_column(Integer)
    tickers_failed: Mapped[int | None] = mapped_column(Integer)
    error: Mapped[str | None] = mapped_column(Text)
```

Migrasi awal: di `alembic/versions/0001_init.py`, isi `upgrade()` dengan `op.execute(SQL)` di mana `SQL` adalah skrip dari bagian 8, dan `downgrade()` dengan `DROP TABLE ... CASCADE` untuk seluruh tabel. Jalankan dengan `alembic upgrade head`.

### 14.7 Job fundamental, aksi korporasi, dan seed aturan

Tiga model tambahan untuk `backend/core/models.py` (tabel sudah ada di skema bagian 8):

```python
class FundamentalsSnapshot(Base):
    __tablename__ = "fundamentals_snapshot"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    as_of: Mapped[date] = mapped_column(Date, primary_key=True)
    market_cap: Mapped[float | None] = mapped_column(Numeric(28, 2))
    pe_ttm: Mapped[float | None] = _float()
    pb: Mapped[float | None] = _float()
    ps: Mapped[float | None] = _float()
    ev_ebitda: Mapped[float | None] = _float()
    roe: Mapped[float | None] = _float()
    roa: Mapped[float | None] = _float()
    gross_margin: Mapped[float | None] = _float()
    op_margin: Mapped[float | None] = _float()
    net_margin: Mapped[float | None] = _float()
    debt_equity: Mapped[float | None] = _float()
    current_ratio: Mapped[float | None] = _float()
    div_yield: Mapped[float | None] = _float()
    payout: Mapped[float | None] = _float()
    revenue_ttm: Mapped[float | None] = mapped_column(Numeric(28, 2))
    net_income_ttm: Mapped[float | None] = mapped_column(Numeric(28, 2))
    fcf_ttm: Mapped[float | None] = mapped_column(Numeric(28, 2))
    rev_growth_yoy: Mapped[float | None] = _float()
    eps_growth_yoy: Mapped[float | None] = _float()
    na_reason: Mapped[dict] = mapped_column(JSONB, default=dict)


class FinancialStatement(Base):
    __tablename__ = "financial_statements"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    period_end: Mapped[date] = mapped_column(Date, primary_key=True)
    period_type: Mapped[str] = mapped_column(String, primary_key=True)
    statement: Mapped[str] = mapped_column(String, primary_key=True)
    item: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[float | None] = mapped_column(Numeric(28, 2))
    currency: Mapped[str] = mapped_column(String, default="IDR")
    source: Mapped[str] = mapped_column(String, default="yfinance")


class CorporateAction(Base):
    __tablename__ = "corporate_actions"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    action_date: Mapped[date] = mapped_column(Date, primary_key=True)
    kind: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[float] = mapped_column(Numeric(18, 6))
```

`backend/worker/fundamentals.py` (hitung rasio dari laporan kuartalan)

```python
import math

import pandas as pd

FIN_NA = {"debt_equity", "current_ratio", "ev_ebitda", "gross_margin"}   # tidak berlaku bagi bank dll.
LOSS_COLS = {"pe_ttm", "payout"}                                         # kosong karena laba negatif
LIMITS = {"pe_ttm": (0, 1000), "pb": (0, 100), "roe": (-5, 5)}            # di luar rentang = n/a


def _row(df: pd.DataFrame | None, items: tuple[str, ...]) -> pd.Series | None:
    """df kuartalan yfinance: baris = item, kolom = tanggal. Urut dari terbaru."""
    if df is None or df.empty:
        return None
    for it in items:
        if it in df.index:
            s = pd.to_numeric(df.loc[it], errors="coerce").dropna()
            if len(s):
                return s.sort_index(ascending=False)
    return None


def ttm(df, *items):
    s = _row(df, items)
    return float(s.iloc[:4].sum()) if s is not None and len(s) >= 4 else None


def latest(df, *items):
    s = _row(df, items)
    return float(s.iloc[0]) if s is not None else None


def yoy(df, *items):
    """Kuartal terakhir dibanding kuartal sama tahun lalu (butuh 5 kuartal, basis > 0)."""
    s = _row(df, items)
    if s is None or len(s) < 5 or s.iloc[4] <= 0:
        return None
    return float(s.iloc[0] / s.iloc[4] - 1)


def _div(a, b):
    return a / b if a is not None and b is not None and b > 0 else None


def compute_snapshot(*, price, shares, is_financial, info, income, balance, cashflow,
                     fx=None, div12=0.0) -> dict:
    k = fx if (info.get("financialCurrency") == "USD" and fx) else 1.0
    scale = lambda v: None if v is None else v * k   # noqa: E731

    rev = scale(ttm(income, "Total Revenue", "Operating Revenue"))
    ni = scale(ttm(income, "Net Income", "Net Income Common Stockholders"))
    gp = scale(ttm(income, "Gross Profit"))
    oi = scale(ttm(income, "Operating Income"))
    ebitda = scale(ttm(income, "EBITDA", "Normalized EBITDA"))
    fcf = scale(ttm(cashflow, "Free Cash Flow"))
    equity = scale(latest(balance, "Stockholders Equity", "Common Stock Equity"))
    assets = scale(latest(balance, "Total Assets"))
    debt = scale(latest(balance, "Total Debt"))
    cash = scale(latest(balance, "Cash And Cash Equivalents"))
    cur_a = latest(balance, "Current Assets")
    cur_l = latest(balance, "Current Liabilities")

    mcap = price * shares if price and shares else None
    ev = mcap + (debt or 0) - (cash or 0) if mcap is not None else None
    m = {
        "market_cap": mcap,
        "pe_ttm": _div(mcap, ni), "pb": _div(mcap, equity), "ps": _div(mcap, rev),
        "ev_ebitda": _div(ev, ebitda),
        "roe": _div(ni, equity), "roa": _div(ni, assets),
        "gross_margin": _div(gp, rev), "op_margin": _div(oi, rev), "net_margin": _div(ni, rev),
        "debt_equity": _div(debt, equity), "current_ratio": _div(cur_a, cur_l),
        "div_yield": (div12 / price) if price else None,
        "payout": _div(div12 * shares, ni) if shares else None,
        "revenue_ttm": rev, "net_income_ttm": ni, "fcf_ttm": fcf,
        "rev_growth_yoy": yoy(income, "Total Revenue", "Operating Revenue"),
        "eps_growth_yoy": yoy(income, "Net Income", "Net Income Common Stockholders"),
    }
    # roe boleh negatif (laba rugi), tetapi ekuitas harus positif (ditangani _div)
    if ni is not None and equity is not None and equity > 0:
        m["roe"] = ni / equity
    for col, (lo, hi) in LIMITS.items():            # sanity check bagian 6
        if m[col] is not None and not (lo < m[col] < hi):
            m[col] = None

    has_data = any(v is not None for v in (rev, ni, equity, assets))
    na: dict[str, str] = {}
    for col, v in m.items():
        if v is not None or col == "market_cap":
            continue
        if is_financial and col in FIN_NA:
            na[col] = "bank"
        elif not has_data:
            na[col] = "no data"
        elif col in LOSS_COLS and ni is not None and ni <= 0:
            na[col] = "loss"
        else:
            na[col] = "n/a"
    clean = {c: (None if v is None or (isinstance(v, float) and not math.isfinite(v)) else float(v))
             for c, v in m.items()}
    return {**clean, "na_reason": na}
```

`backend/worker/jobs/ingest_fundamentals.py`

```python
import time
from datetime import date, timedelta

import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import FinancialStatement, FundamentalsSnapshot
from providers.base import DataProvider
from providers.yahoo import YahooProvider
from worker.fundamentals import compute_snapshot
from worker.runlog import logged_run

FAIL_TOLERANCE = 0.30


def _usd_idr(provider: DataProvider) -> float | None:
    df = provider.fetch_prices(["IDR=X"], start=(date.today() - timedelta(days=10)).isoformat())
    return None if df.empty else float(df.sort_values("date")["close"].iloc[-1])


def _stmt_rows(ticker: str, df: pd.DataFrame | None, stmt: str, currency: str) -> list[dict]:
    rows: list[dict] = []
    if df is None or df.empty:
        return rows
    for item in df.index:
        series = pd.to_numeric(df.loc[item], errors="coerce")
        for col, v in series.items():
            if pd.notna(v):
                rows.append({"ticker": ticker, "period_end": pd.Timestamp(col).date(),
                             "period_type": "Q", "statement": stmt, "item": str(item),
                             "value": float(v), "currency": currency, "source": "yfinance"})
    return rows


def run(provider: DataProvider | None = None, limit: int | None = None) -> dict:
    provider = provider or YahooProvider()
    with logged_run("fundamentals") as res:
        with SessionLocal() as s:
            companies = s.execute(text("""
                SELECT c.ticker, c.yahoo_symbol, c.shares_outstanding, c.is_financial,
                       (SELECT close FROM prices_daily p WHERE p.ticker = c.ticker
                        ORDER BY trade_date DESC LIMIT 1) AS close
                FROM companies c WHERE c.is_active ORDER BY c.ticker""")).mappings().all()
            div12 = dict(s.execute(text("""
                SELECT ticker, sum(value) FROM corporate_actions
                WHERE kind = 'dividend' AND action_date >= CURRENT_DATE - 365
                GROUP BY ticker""")).all())
            fx = _usd_idr(provider)
            failed = 0
            todo = companies[:limit] if limit else companies
            for n, c in enumerate(todo, start=1):
                try:
                    data = provider.fetch_fundamentals(c["yahoo_symbol"])
                except Exception:  # noqa: BLE001
                    failed += 1
                    continue
                info = data["info"]
                shares = info.get("sharesOutstanding") or c["shares_outstanding"]
                if shares and shares != c["shares_outstanding"]:
                    s.execute(text("UPDATE companies SET shares_outstanding = :sh WHERE ticker = :t"),
                              {"sh": int(shares), "t": c["ticker"]})
                snap = compute_snapshot(
                    price=float(c["close"]) if c["close"] is not None else None,
                    shares=int(shares) if shares else None, is_financial=c["is_financial"],
                    info=info, income=data["income"], balance=data["balance"],
                    cashflow=data["cashflow"], fx=fx, div12=float(div12.get(c["ticker"], 0.0)))
                res["rows"] += upsert(s, FundamentalsSnapshot,
                                      [{"ticker": c["ticker"], "as_of": date.today(), **snap}],
                                      ["ticker", "as_of"])
                cur = info.get("financialCurrency") or "IDR"
                stmts = (_stmt_rows(c["ticker"], data["income"], "IS", cur)
                         + _stmt_rows(c["ticker"], data["balance"], "BS", cur)
                         + _stmt_rows(c["ticker"], data["cashflow"], "CF", cur))
                upsert(s, FinancialStatement, stmts,
                       ["ticker", "period_end", "period_type", "statement", "item"])
                if n % 50 == 0:
                    s.commit()          # simpan bertahap agar run panjang tidak sia-sia
                time.sleep(0.5)
            s.commit()
            res["failed"] = failed
            if todo and failed / len(todo) > FAIL_TOLERANCE:
                raise RuntimeError(f"{failed} dari {len(todo)} emiten gagal")
    return res
```

`backend/worker/jobs/ingest_actions.py` dan `seed_rules.py`

```python
# ingest_actions.py
from sqlalchemy import select

from core.db import SessionLocal, upsert
from core.models import Company, CorporateAction
from providers.yahoo import YahooProvider
from worker.runlog import logged_run


def run(provider=None) -> dict:
    provider = provider or YahooProvider()
    with logged_run("actions") as res:
        with SessionLocal() as s:
            symbols = list(s.scalars(select(Company.yahoo_symbol).where(Company.is_active)))
            df = provider.fetch_actions(symbols)
            if df.empty:
                return res
            df["ticker"] = df["symbol"].str.removesuffix(".JK")
            rows = [{"ticker": r.ticker, "action_date": r.date, "kind": r.kind, "value": r.value}
                    for r in df.itertuples()]
            res["rows"] = upsert(s, CorporateAction, rows, ["ticker", "action_date", "kind"])
            s.commit()
    return res
```

```python
# seed_rules.py  (isi tabel watchlists dari YAML; wajib sebelum run_rules karena ada foreign key)
from sqlalchemy import text

from core.db import SessionLocal
from core.rules import load_rules


def run() -> dict:
    with SessionLocal() as s:
        for i, r in enumerate(load_rules("watchlists")):
            s.execute(text("""
                INSERT INTO watchlists (slug, name, description, rule_expr, sort_order)
                VALUES (:slug, :name, :desc, :expr, :ord)
                ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name,
                  description = EXCLUDED.description, rule_expr = EXCLUDED.rule_expr,
                  sort_order = EXCLUDED.sort_order"""),
                {"slug": r["slug"], "name": r["name"], "desc": r["description"],
                 "expr": " ".join(r["expr"].split()), "ord": i})
        s.commit()
    return {"status": "ok"}
```

Tambahkan sub-perintah ke `worker/cli.py`: `sub.add_parser("seed-rules")` dan cabang `elif args.cmd == "seed-rules": seed_rules.run()`, plus `from worker.jobs import seed_rules`.

Catatan urutan dan operasional:

- **Urutan pertama kali** yang benar: `alembic upgrade head`, `seed` (harus mengisi 11 baris `sectors` dan `companies`), `seed-rules`, backfill harga, lalu `python -c "from worker.jobs import ingest_fundamentals as f; f.run()"` **sebelum** pipeline harian pertama. Peta pasar membutuhkan `companies.shares_outstanding`, dan kolom itu baru terisi oleh job fundamental.
- `ingest_actions` memanggil yfinance per ticker (sekitar 800 permintaan, beberapa menit). Bila terkena batas laju, keluarkan dari daftar `steps` di `pipeline.py` dan jadwalkan mingguan di `worker/main.py`.
- Pertumbuhan `rev_growth_yoy` dan `eps_growth_yoy` adalah perbandingan kuartal terakhir dengan kuartal yang sama tahun lalu (bukan TTM), karena yfinance biasanya hanya memberi sekitar 5 kuartal. Tampilkan definisi ini di halaman Start Here.

### 14.8 Router saham dan watchlist

`backend/app/routers/stocks.py`

```python
from fastapi import APIRouter, Query
from sqlalchemy import text

from app.errors import ApiError
from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["stocks"])
RANGE_DAYS = {"1m": 31, "3m": 93, "1y": 366, "5y": 1830, "max": 36500}

SQL_STOCK = text("""
    SELECT c.ticker, c.name, s.name AS sector, p.close, p.trade_date,
           to_jsonb(i) - 'ticker' - 'trade_date' AS ind,
           to_jsonb(f) - 'ticker' - 'as_of' AS fun
    FROM companies c
    LEFT JOIN sectors s ON s.id = c.sector_id
    JOIN LATERAL (SELECT * FROM prices_daily WHERE ticker = c.ticker
                  ORDER BY trade_date DESC LIMIT 1) p ON TRUE
    LEFT JOIN indicators_daily i ON i.ticker = c.ticker AND i.trade_date = p.trade_date
    LEFT JOIN LATERAL (SELECT * FROM fundamentals_snapshot x WHERE x.ticker = c.ticker
                       ORDER BY as_of DESC LIMIT 1) f ON TRUE
    WHERE c.ticker = :t
""")


@cached()
def build_stock(ticker: str) -> dict:
    with SessionLocal() as s:
        r = s.execute(SQL_STOCK, {"t": ticker}).mappings().first()
        if r is None:
            raise ApiError(404, "not_found", f"Ticker {ticker} tidak ditemukan")
        sigs = s.execute(text("""
            SELECT trade_date, kind, detail FROM signals
            WHERE ticker = :t ORDER BY trade_date DESC, kind LIMIT 20"""), {"t": ticker}).mappings().all()
    fun = dict(r["fun"] or {})
    na = fun.pop("na_reason", {}) or {}
    return {"as_of": r["trade_date"], "ticker": r["ticker"], "name": r["name"],
            "sector": r["sector"], "close": float(r["close"]),
            "indicators": r["ind"] or {}, "fundamentals": fun, "na_reason": na,
            "signals": [dict(x) for x in sigs]}


@cached()
def build_prices(ticker: str, range_: str) -> dict:
    with SessionLocal() as s:
        rows = s.execute(text("""
            SELECT trade_date AS time, open, high, low, close, volume FROM prices_daily
            WHERE ticker = :t AND NOT is_suspect
              AND trade_date >= CURRENT_DATE - CAST(:d AS integer)
            ORDER BY trade_date"""), {"t": ticker, "d": RANGE_DAYS[range_]}).mappings().all()
    return {"ticker": ticker, "range": range_,
            "data": [{k: (float(v) if hasattr(v, "is_finite") else v) for k, v in dict(r).items()}
                     for r in rows]}


@router.get("/stocks/{ticker}")
def stock(ticker: str):
    return build_stock(ticker=ticker.upper())


@router.get("/stocks/{ticker}/prices")
def prices(ticker: str, range: str = Query("1y", pattern="^(1m|3m|1y|5y|max)$")):
    return build_prices(ticker=ticker.upper(), range_=range)
```

`backend/app/routers/watchlists.py`

```python
from datetime import date as Date

from fastapi import APIRouter, Query
from sqlalchemy import text

from app.errors import ApiError
from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["watchlists"])


@cached()
def build_list() -> dict:
    with SessionLocal() as s:
        rows = s.execute(text("""
            SELECT w.slug, w.name, w.description, w.rule_expr,
                   (SELECT count(*) FROM watchlist_members m WHERE m.slug = w.slug
                      AND m.trade_date = (SELECT max(trade_date) FROM watchlist_members)) AS members
            FROM watchlists w ORDER BY w.sort_order, w.slug""")).mappings().all()
    return {"data": [dict(r) for r in rows]}


@cached()
def build_watchlist(slug: str, on: str | None) -> dict:
    with SessionLocal() as s:
        w = s.execute(text("SELECT slug, name, description, rule_expr FROM watchlists WHERE slug = :s"),
                      {"s": slug}).mappings().first()
        if w is None:
            raise ApiError(404, "not_found", f"Daftar '{slug}' tidak ada")
        rows = s.execute(text("""
            SELECT m.trade_date, m.rank, c.ticker, c.name, sc.name AS sector, p.close,
                   i.ret_1d, i.ret_1m, i.rs_rating, i.close_vs_high
            FROM watchlist_members m
            JOIN companies c ON c.ticker = m.ticker
            LEFT JOIN sectors sc ON sc.id = c.sector_id
            JOIN prices_daily p ON p.ticker = m.ticker AND p.trade_date = m.trade_date
            LEFT JOIN (SELECT *, close_ref / NULLIF(hi_52w, 0) - 1 AS close_vs_high FROM (
                         SELECT i0.*, p0.close AS close_ref FROM indicators_daily i0
                         JOIN prices_daily p0 ON p0.ticker = i0.ticker
                              AND p0.trade_date = i0.trade_date) z) i
                   ON i.ticker = m.ticker AND i.trade_date = m.trade_date
            WHERE m.slug = :s
              AND m.trade_date = COALESCE(CAST(:d AS date),
                    (SELECT max(trade_date) FROM watchlist_members WHERE slug = :s))
            ORDER BY m.rank"""), {"s": slug, "d": on}).mappings().all()
    data = [{k: (float(v) if hasattr(v, "is_finite") else v) for k, v in dict(r).items()}
            for r in rows]
    return {"as_of": data[0]["trade_date"] if data else on, "watchlist": dict(w),
            "count": len(data), "data": data}


@router.get("/watchlists")
def list_watchlists():
    return build_list()


@router.get("/watchlists/{slug}")
def watchlist(slug: str, date: Date | None = Query(None)):
    return build_watchlist(slug=slug, on=date.isoformat() if date else None)
```

Dua router ini sudah terdaftar di `app/main.py` (bagian 14.5). Endpoint `/screens` (17 screen) mengikuti pola `build_screener`: muat `rules/screens.yaml`, jalankan `apply_rule` pada DataFrame yang sama dengan screener, dan kembalikan `description`, `expr`, serta daftar saham yang lolos.

### 14.9 Frontend: aplikasi, Screener, dan Daily Feed

Rute didefinisikan langsung di `App.tsx` (berkas `routes.tsx` di pohon folder tidak diperlukan pada tahap ini). Tambahkan halaman lain (Watchlist, Portfolio, Stock, Start) dengan pola `lazy` yang sama.

`frontend/src/styles/index.css` dan `tailwind.config.ts`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root { --bg:#F7F8FA; --surface:#FFFFFF; --border:#E3E6EB; --text:#141821; --muted:#6B7280;
        --up:#16A34A; --down:#DC2626; --accent:#2563EB; }
.dark { --bg:#0D1117; --surface:#161B22; --border:#262D36; --text:#E6EAF0; --muted:#8B95A5;
        --up:#22C55E; --down:#F87171; --accent:#60A5FA; }
body { background: var(--bg); color: var(--text); font-family: Inter, system-ui, sans-serif; }
```

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
} satisfies Config;
```

`frontend/src/main.tsx` dan `App.tsx`

```tsx
// main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./styles/index.css";

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
);
```

```tsx
// App.tsx
import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import AppShell from "./components/layout/AppShell";

const Explore = lazy(() => import("./pages/Explore"));
const Screener = lazy(() => import("./pages/Screener"));
const Feed = lazy(() => import("./pages/Feed"));

export default function App() {
  return (
    <AppShell>
      <Suspense fallback={<div className="p-4 text-[--muted]">Memuat…</div>}>
        <Routes>
          <Route path="/" element={<Explore />} />
          <Route path="/screener" element={<Navigate to="/screener/valuation" replace />} />
          <Route path="/screener/:menu" element={<Screener />} />
          <Route path="/feed" element={<Feed />} />
          <Route path="*" element={<p className="p-4">Halaman tidak ditemukan.</p>} />
        </Routes>
      </Suspense>
    </AppShell>
  );
}
```

`frontend/src/api/types.ts` (tambahkan) dan `hooks.ts` (tambahkan)

```ts
// types.ts
export interface Meta {
  as_of: string | null;
  active_companies: number;
  last_run: { job: string; status: string; finished_at: string | null } | null;
}
export type NaReasonKey = "bank" | "no data" | "loss" | "n/a";
export interface ScreenerRow {
  ticker: string;
  name: string;
  sector: string | null;
  score: number | null;
  na_reason: Record<string, NaReasonKey>;
  [col: string]: unknown;
}
export interface ScreenerResponse {
  as_of: string | null;
  menu: string;
  columns: string[];
  data: ScreenerRow[];
}
export interface Filters { sector: string; minMcap: number; minValue: number; q: string; limit: number }
export interface FeedItem {
  trade_date: string; ticker: string; name: string; sector: string | null;
  kind: string; detail: Record<string, number | null>;
}
export interface FeedResponse { days: number; data: FeedItem[] }
```

```ts
// hooks.ts (tambahan)
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import type { FeedResponse, Filters, Meta, ScreenerResponse } from "./types";

export const useMeta = () =>
  useQuery({ queryKey: ["meta"], queryFn: () => api<Meta>("/meta"), staleTime: 5 * 60_000 });

export function useScreener(menu: string, f: Filters) {
  const qs = new URLSearchParams({
    menu, min_mcap: String(f.minMcap), min_value: String(f.minValue), limit: String(f.limit),
  });
  if (f.sector) qs.set("sector", f.sector);
  if (f.q) qs.set("q", f.q);
  return useQuery({
    queryKey: ["screener", qs.toString()],
    queryFn: () => api<ScreenerResponse>(`/screener?${qs}`),
    staleTime: 5 * 60_000,
    placeholderData: keepPreviousData,
  });
}

export const useFeed = (days: number, kind: string) =>
  useQuery({
    queryKey: ["feed", days, kind],
    queryFn: () => api<FeedResponse>(`/feed?days=${days}${kind ? `&kind=${kind}` : ""}`),
    staleTime: 5 * 60_000,
  });
```

`frontend/src/lib/sectors.ts` dan `lib/csv.ts`

```ts
// sectors.ts: kode ini juga isi tabel sectors di database (sector_map.csv memakai kode yang sama)
export const SECTORS: Record<string, string> = {
  ENE: "Energy", BAS: "Basic Materials", IND: "Industrials", NCY: "Consumer Non-Cyclicals",
  CYC: "Consumer Cyclicals", HLT: "Healthcare", FIN: "Financials",
  PRO: "Properties & Real Estate", TEC: "Technology", INF: "Infrastructures",
  TRA: "Transportation & Logistics",
};
```

```ts
// csv.ts
export function toCsv(columns: string[], rows: Record<string, unknown>[]): string {
  const esc = (v: unknown) => {
    const s = v == null ? "" : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [columns.join(","), ...rows.map((r) => columns.map((c) => esc(r[c])).join(","))].join("\n");
}

export function download(name: string, text: string) {
  const url = URL.createObjectURL(new Blob([text], { type: "text/csv;charset=utf-8" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}
```

`frontend/src/components/layout/AppShell.tsx`

```tsx
import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import { useMeta } from "../../api/hooks";

const NAV = [
  { to: "/", label: "Explore" },
  { to: "/screener/valuation", label: "Screener" },
  { to: "/feed", label: "Daily Feed" },
];

export default function AppShell({ children }: { children: ReactNode }) {
  const { data } = useMeta();
  return (
    <div className="flex min-h-screen flex-col">
      <header className="flex flex-wrap items-center gap-4 border-b border-[--border] px-4 py-2">
        <span className="font-semibold">IDX Witcher</span>
        <nav className="flex gap-3 text-sm">
          {NAV.map((n) => (
            <NavLink key={n.to} to={n.to} end={n.to === "/"}
              className={({ isActive }) => (isActive ? "font-semibold text-[--accent]" : "text-[--muted]")}>
              {n.label}
            </NavLink>
          ))}
        </nav>
        <button className="ml-auto text-sm" aria-label="Ganti tema"
          onClick={() => document.documentElement.classList.toggle("dark")}>◐</button>
      </header>
      <main className="flex-1">{children}</main>
      <footer className="border-t border-[--border] px-4 py-3 text-xs text-[--muted]">
        Data harian (end-of-day) per {data?.as_of ?? "–"}. Sumber: Yahoo Finance. Bukan saran
        investasi; hasil adalah filter mekanis untuk tujuan edukasi.
      </footer>
    </div>
  );
}
```

`frontend/src/components/table/DataTable.tsx`

```tsx
import { useMemo, useState } from "react";
import {
  flexRender, getCoreRowModel, getSortedRowModel, useReactTable,
  type ColumnDef, type SortingState,
} from "@tanstack/react-table";
import type { ScreenerRow } from "../../api/types";
import { fmtNum, fmtPct, fmtRp } from "../../lib/format";
import { NaCell } from "./NaCell";

const TEXT = new Set(["ticker", "name", "sector"]);
const PCT = new Set(["ret_1d", "ret_1m", "ret_3m", "ret_ytd", "ret_1y", "roe", "roa", "gross_margin",
  "op_margin", "net_margin", "div_yield", "payout", "rev_growth_yoy", "eps_growth_yoy"]);
const RP = new Set(["market_cap", "revenue_ttm", "net_income_ttm", "fcf_ttm", "value_avg20"]);
const LABEL: Record<string, string> = {
  ticker: "Ticker", name: "Nama", sector: "Sektor", market_cap: "Market cap", close: "Harga",
  pe_ttm: "PER", pb: "PBV", ps: "PSR", ev_ebitda: "EV/EBITDA", div_yield: "Dividen",
  roe: "ROE", roa: "ROA", gross_margin: "Margin kotor", op_margin: "Margin operasi",
  net_margin: "Margin bersih", debt_equity: "DER", current_ratio: "Current ratio",
  payout: "Payout", rev_growth_yoy: "Pertumbuhan pendapatan", eps_growth_yoy: "Pertumbuhan laba",
  revenue_ttm: "Pendapatan TTM", net_income_ttm: "Laba bersih TTM", fcf_ttm: "FCF TTM",
  ret_1d: "1D", ret_1m: "1M", ret_3m: "3M", ret_ytd: "YTD", ret_1y: "1Y", rs_rating: "RS",
  value_avg20: "Nilai transaksi 20D", score: "Skor",
};

function renderCell(col: string, row: ScreenerRow) {
  const v = row[col];
  if (v == null) return <NaCell reason={row.na_reason?.[col]} />;
  if (typeof v !== "number") return String(v);
  if (PCT.has(col)) return fmtPct(v, 1);
  if (RP.has(col)) return fmtRp(v);
  return fmtNum(v);
}

export function DataTable({ columns, rows }: { columns: string[]; rows: ScreenerRow[] }) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const defs = useMemo<ColumnDef<ScreenerRow>[]>(
    () => columns.map((c) => ({
      id: c,
      header: LABEL[c] ?? c,
      accessorFn: (r: ScreenerRow) => (r[c] == null ? undefined : typeof r[c] === "number" ? (r[c] as number) : String(r[c])),
      cell: ({ row }) => renderCell(c, row.original),
      sortUndefined: "last" as const,
    })),
    [columns],
  );
  const table = useReactTable({
    data: rows, columns: defs, state: { sorting }, onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(), getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="overflow-x-auto rounded border border-[--border]">
      <table className="w-full text-sm tabular-nums">
        <thead className="bg-[--surface] text-left">
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((h) => {
                const dir = h.column.getIsSorted();
                return (
                  <th key={h.id} onClick={h.column.getToggleSortingHandler()}
                    aria-sort={dir === "asc" ? "ascending" : dir === "desc" ? "descending" : "none"}
                    className={`cursor-pointer select-none whitespace-nowrap px-3 py-2 ${TEXT.has(h.column.id) ? "" : "text-right"} ${h.column.id === "ticker" ? "sticky left-0 bg-[--surface]" : ""}`}>
                    {flexRender(h.column.columnDef.header, h.getContext())}
                    {dir === "asc" ? " ▲" : dir === "desc" ? " ▼" : ""}
                  </th>
                );
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((r) => (
            <tr key={r.id} className="border-t border-[--border]">
              {r.getVisibleCells().map((c) => (
                <td key={c.id}
                  className={`whitespace-nowrap px-3 py-1.5 ${TEXT.has(c.column.id) ? "" : "text-right"} ${c.column.id === "ticker" ? "sticky left-0 bg-[--bg] font-medium" : ""}`}>
                  {flexRender(c.column.columnDef.cell, c.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

`frontend/src/components/table/FilterBar.tsx`

```tsx
import { useSearchParams } from "react-router-dom";
import type { Filters } from "../../api/types";
import { SECTORS } from "../../lib/sectors";

const MCAP: [string, number][] = [["Any", 0], ["≥ Rp1 T", 1e12], ["≥ Rp10 T", 1e13], ["≥ Rp50 T", 5e13]];
const VALUE: [string, number][] = [["Any", 0], ["≥ Rp1 M", 1e9], ["≥ Rp10 M", 1e10], ["≥ Rp50 M", 5e10]];
const LIMITS: [string, number][] = [["30", 30], ["50", 50], ["100", 100], ["All", 0]];

/** Filter disimpan di URL agar tautan dapat dibagikan. */
export function useFilters(): [Filters, (patch: Partial<Filters>) => void] {
  const [sp, setSp] = useSearchParams();
  const f: Filters = {
    sector: sp.get("sector") ?? "",
    minMcap: Number(sp.get("mcap") ?? 0),
    minValue: Number(sp.get("value") ?? 0),
    q: sp.get("q") ?? "",
    limit: Number(sp.get("limit") ?? 50),
  };
  const set = (patch: Partial<Filters>) => {
    const n = { ...f, ...patch };
    const p = new URLSearchParams();
    if (n.sector) p.set("sector", n.sector);
    if (n.minMcap) p.set("mcap", String(n.minMcap));
    if (n.minValue) p.set("value", String(n.minValue));
    if (n.q) p.set("q", n.q);
    p.set("limit", String(n.limit));
    setSp(p, { replace: true });
  };
  return [f, set];
}

const sel = "rounded border border-[--border] bg-[--surface] px-2 py-1 text-sm";

export function FilterBar({ filters, onChange }: { filters: Filters; onChange: (p: Partial<Filters>) => void }) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <select className={sel} value={filters.sector} aria-label="Sektor"
        onChange={(e) => onChange({ sector: e.target.value })}>
        <option value="">Semua sektor</option>
        {Object.entries(SECTORS).map(([code, name]) => <option key={code} value={code}>{name}</option>)}
      </select>
      <select className={sel} value={filters.minMcap} aria-label="Market cap minimum"
        onChange={(e) => onChange({ minMcap: Number(e.target.value) })}>
        {MCAP.map(([l, v]) => <option key={v} value={v}>Market cap {l}</option>)}
      </select>
      <select className={sel} value={filters.minValue} aria-label="Nilai transaksi minimum"
        onChange={(e) => onChange({ minValue: Number(e.target.value) })}>
        {VALUE.map(([l, v]) => <option key={v} value={v}>Nilai transaksi {l}</option>)}
      </select>
      <select className={sel} value={filters.limit} aria-label="Jumlah baris"
        onChange={(e) => onChange({ limit: Number(e.target.value) })}>
        {LIMITS.map(([l, v]) => <option key={v} value={v}>{l} baris</option>)}
      </select>
      <input className={`${sel} w-40`} placeholder="Cari ticker/nama" value={filters.q}
        onChange={(e) => onChange({ q: e.target.value })} />
    </div>
  );
}
```

`frontend/src/pages/Screener.tsx`

```tsx
import { Link, useLocation, useParams } from "react-router-dom";
import { useScreener } from "../api/hooks";
import { DataTable } from "../components/table/DataTable";
import { FilterBar, useFilters } from "../components/table/FilterBar";
import { download, toCsv } from "../lib/csv";

const MENUS: [string, string][] = [
  ["overview", "Overview"], ["valuation", "Valuation"], ["profitability", "Profitability"],
  ["growth", "Growth"], ["dividends", "Dividends"], ["balance-sheet", "Balance Sheet"],
  ["cash-flow", "Cash Flow"], ["quality", "Quality"], ["efficiency", "Efficiency"],
  ["momentum", "Momentum"], ["technical", "Technical"], ["liquidity", "Liquidity"],
  ["size", "Size"], ["ownership", "Ownership"],
];

export default function Screener() {
  const { menu = "valuation" } = useParams();
  const { search } = useLocation();
  const [filters, setFilters] = useFilters();
  const { data, isLoading, error, refetch, isFetching } = useScreener(menu, filters);

  return (
    <section className="space-y-3 p-4">
      <nav className="flex gap-2 overflow-x-auto pb-1 text-sm" aria-label="Menu screener">
        {MENUS.map(([id, label]) => (
          <Link key={id} to={{ pathname: `/screener/${id}`, search }}
            className={`whitespace-nowrap rounded px-3 py-1 ${id === menu ? "bg-[--accent] text-white" : "border border-[--border]"}`}>
            {label}
          </Link>
        ))}
      </nav>
      <FilterBar filters={filters} onChange={setFilters} />
      {isLoading && <div className="h-64 animate-pulse rounded bg-[--surface]" />}
      {error && <button className="underline" onClick={() => refetch()}>Gagal memuat. Coba lagi</button>}
      {data && (
        <>
          <div className="flex items-center justify-between text-xs text-[--muted]">
            <span>
              {data.data.length} saham · harga per {data.as_of ?? "–"}{isFetching ? " · memperbarui…" : ""}
            </span>
            <button className="underline"
              onClick={() => download(`idx-witcher-${menu}.csv`, toCsv(data.columns, data.data))}>
              Ekspor CSV
            </button>
          </div>
          <DataTable columns={data.columns} rows={data.data} />
        </>
      )}
    </section>
  );
}
```

`frontend/src/pages/Feed.tsx`

```tsx
import { useMemo, useState } from "react";
import { useFeed } from "../api/hooks";
import type { FeedItem } from "../api/types";
import { fmtNum, fmtPct } from "../lib/format";

const KIND: Record<string, string> = {
  new_high: "High 52 minggu baru", new_low: "Low 52 minggu baru",
  volume_surge: "Lonjakan volume", big_move: "Pergerakan besar",
  breakdown_sma50: "Turun di bawah SMA50", breakout_sma50: "Naik di atas SMA50",
  breakdown_sma200: "Turun di bawah SMA200", breakout_sma200: "Naik di atas SMA200",
};

export default function Feed() {
  const [kind, setKind] = useState("");
  const { data, isLoading, error } = useFeed(5, kind);
  const groups = useMemo(() => {
    const m = new Map<string, FeedItem[]>();
    for (const i of data?.data ?? []) m.set(i.trade_date, [...(m.get(i.trade_date) ?? []), i]);
    return [...m.entries()];
  }, [data]);

  return (
    <section className="space-y-4 p-4">
      <select className="rounded border border-[--border] bg-[--surface] px-2 py-1 text-sm"
        value={kind} onChange={(e) => setKind(e.target.value)} aria-label="Jenis sinyal">
        <option value="">Semua sinyal</option>
        {Object.entries(KIND).map(([k, l]) => <option key={k} value={k}>{l}</option>)}
      </select>
      {isLoading && <div className="h-40 animate-pulse rounded bg-[--surface]" />}
      {error && <p>Gagal memuat feed.</p>}
      {groups.map(([day, items]) => (
        <div key={day}>
          <h2 className="mb-2 text-sm font-semibold">{day}</h2>
          <ul className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((i) => (
              <li key={`${i.ticker}-${i.kind}`} className="rounded border border-[--border] bg-[--surface] p-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="font-medium">{i.ticker}</span>
                  <span className="rounded bg-[--bg] px-2 py-0.5 text-xs">{KIND[i.kind] ?? i.kind}</span>
                </div>
                <div className="text-xs text-[--muted]">{i.name}</div>
                <div className="mt-1 text-xs tabular-nums">
                  {i.detail.ret_1d != null && <>Perubahan {fmtPct(i.detail.ret_1d)} </>}
                  {i.kind === "volume_surge" && i.detail.vol_ratio != null && <>· volume {fmtNum(i.detail.vol_ratio)}× rata-rata</>}
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
      {data && groups.length === 0 && <p className="text-[--muted]">Tidak ada sinyal pada 5 sesi terakhir.</p>}
    </section>
  );
}
```

Setelah backend berjalan, jalankan `npm run dev`, buka `http://localhost:5173`, dan periksa berurutan: footer menampilkan tanggal `as_of`, peta pasar terisi, `/screener/valuation` menampilkan tabel dengan sel abu-abu beralasan, dan `/feed` menampilkan sinyal. Bila peta kosong, periksa dulu `companies.shares_outstanding` (diisi job fundamental) dan hasil `/api/v1/meta`.

### 14.10 Seed sektor dan sync\_companies

Tiga berkas data di `backend/data/` dan satu job menyiapkan tabel `sectors` dan `companies` yang menjadi fondasi semua fitur lain.

`backend/data/sectors.csv` (11 sektor IDX-IC; kode ini juga dipakai frontend di `lib/sectors.ts`)

```text
id,code,name
1,ENE,Energy
2,BAS,Basic Materials
3,IND,Industrials
4,NCY,Consumer Non-Cyclicals
5,CYC,Consumer Cyclicals
6,HLT,Healthcare
7,FIN,Financials
8,PRO,Properties & Real Estate
9,TEC,Technology
10,INF,Infrastructures
11,TRA,Transportation & Logistics
```

`backend/data/companies_seed.csv` (contoh 25 emiten agar sistem bisa dijalankan untuk uji; verifikasi nama dan sektor terhadap klasifikasi IDX-IC resmi sebelum dipakai)

```text
ticker,name,sector_code
BBCA,Bank Central Asia Tbk.,FIN
BBRI,Bank Rakyat Indonesia (Persero) Tbk.,FIN
BMRI,Bank Mandiri (Persero) Tbk.,FIN
BBNI,Bank Negara Indonesia (Persero) Tbk.,FIN
BRIS,Bank Syariah Indonesia Tbk.,FIN
TLKM,Telkom Indonesia (Persero) Tbk.,INF
EXCL,XL Axiata Tbk.,INF
TOWR,Sarana Menara Nusantara Tbk.,INF
JSMR,Jasa Marga (Persero) Tbk.,INF
ASII,Astra International Tbk.,IND
UNVR,Unilever Indonesia Tbk.,NCY
ICBP,Indofood CBP Sukses Makmur Tbk.,NCY
INDF,Indofood Sukses Makmur Tbk.,NCY
CPIN,Charoen Pokphand Indonesia Tbk.,NCY
KLBF,Kalbe Farma Tbk.,HLT
MIKA,Mitra Keluarga Karyasehat Tbk.,HLT
ANTM,Aneka Tambang Tbk.,BAS
SMGR,Semen Indonesia (Persero) Tbk.,BAS
INCO,Vale Indonesia Tbk.,BAS
PTBA,Bukit Asam Tbk.,ENE
ITMG,Indo Tambangraya Megah Tbk.,ENE
GOTO,GoTo Gojek Tokopedia Tbk.,TEC
BSDE,Bumi Serpong Damai Tbk.,PRO
MAPI,Mitra Adiperkasa Tbk.,CYC
BIRD,Blue Bird Tbk.,TRA
```

Untuk daftar penuh (800+ emiten) ada dua jalur, dan keduanya opsional:

- **`data/idx_listing.xlsx`**: unduh berkas daftar saham dari situs IDX dan simpan dengan nama ini. Bila berkas ada, `sync_companies` memakainya sebagai daftar utama dan menonaktifkan emiten yang tidak lagi tercantum. Nama kolom berkas dapat berubah; sesuaikan konstanta `LISTING_COLS` di kode.
- **`data/sector_map.csv`** (kolom `ticker,sector_code`): pemetaan sektor yang Anda susun dari berkas klasifikasi industri IDX. Isinya menimpa sektor di `companies_seed.csv`. Emiten tanpa sektor dapat diisi otomatis dengan `fill-sectors` (aproksimasi dari profil Yahoo, kode di bawah).

Tambahan untuk antarmuka provider (`providers/base.py` dan `providers/yahoo.py`):

```python
# base.py
    @abstractmethod
    def fetch_profile(self, symbol: str) -> dict:
        """Kunci minimal: sector, industry, sharesOutstanding, longName."""
```

```python
# yahoo.py (di dalam class YahooProvider)
    def fetch_profile(self, symbol):
        info = _retry(lambda: yf.Ticker(symbol).info) or {}
        return {k: info.get(k) for k in ("sector", "industry", "sharesOutstanding", "longName")}
```

`backend/worker/jobs/sync_companies.py`

```python
import time
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import Company, Sector
from providers.base import DataProvider
from providers.yahoo import YahooProvider
from worker.runlog import logged_run

DATA = Path(__file__).resolve().parents[2] / "data"
LISTING_COLS = {"Kode": "ticker", "Nama Perusahaan": "name"}   # sesuaikan dengan berkas IDX terbaru

# Aproksimasi sektor Yahoo ke 11 sektor IDX-IC. Prioritaskan sector_map.csv resmi.
YAHOO_SECTOR = {
    "Energy": "ENE", "Basic Materials": "BAS", "Industrials": "IND", "Consumer Defensive": "NCY",
    "Consumer Cyclical": "CYC", "Healthcare": "HLT", "Financial Services": "FIN",
    "Real Estate": "PRO", "Technology": "TEC", "Utilities": "INF", "Communication Services": "INF",
}
INDUSTRY_TO_CODE = {name: "TRA" for name in (
    "Airlines", "Marine Shipping", "Trucking", "Railroads",
    "Integrated Freight & Logistics", "Airports & Air Services")}


def _load_listing() -> tuple[pd.DataFrame, bool]:
    """Kembalikan (df[ticker, name, sector_code], apakah ini daftar penuh dari IDX)."""
    xlsx = DATA / "idx_listing.xlsx"
    if xlsx.exists():
        df = pd.read_excel(xlsx).rename(columns=LISTING_COLS)[["ticker", "name"]].copy()
        df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()
        df = df[df["ticker"].str.fullmatch(r"[A-Z]{4}")].drop_duplicates("ticker")
        df["sector_code"] = None
        return df, True
    return pd.read_csv(DATA / "companies_seed.csv"), False


def run() -> dict:
    with logged_run("companies") as res:
        with SessionLocal() as s:
            sectors = pd.read_csv(DATA / "sectors.csv")
            upsert(s, Sector, sectors.to_dict("records"), ["id"])
            ids = {c: int(i) for c, i in zip(sectors["code"], sectors["id"])}

            df, full_listing = _load_listing()
            smap_path = DATA / "sector_map.csv"
            if smap_path.exists():
                smap = (pd.read_csv(smap_path).drop_duplicates("ticker")
                        .set_index("ticker")["sector_code"])
                df["sector_code"] = df["ticker"].map(smap).fillna(df["sector_code"])
            unknown = sorted(set(df["sector_code"].dropna()) - set(ids))
            if unknown:
                raise ValueError(f"Kode sektor tidak dikenal: {unknown}")

            df["yahoo_symbol"] = df["ticker"] + ".JK"
            df["is_active"] = True
            has = df["sector_code"].notna()
            with_sec = df[has].assign(
                sector_id=lambda d: d["sector_code"].map(ids).astype(int),
                is_financial=lambda d: d["sector_code"].eq("FIN"),
            )
            base = ["ticker", "yahoo_symbol", "name", "is_active"]
            # emiten tanpa sektor di-upsert tanpa menyentuh sector_id agar hasil fill-sectors tidak terhapus
            n = upsert(s, Company, with_sec[[*base, "sector_id", "is_financial"]].to_dict("records"), ["ticker"])
            n += upsert(s, Company, df[~has][base].to_dict("records"), ["ticker"])
            res["rows"] = n
            if full_listing:
                s.execute(text("UPDATE companies SET is_active = FALSE WHERE NOT (ticker = ANY(:keep))"),
                          {"keep": df["ticker"].tolist()})
            s.commit()
    return res


def fill_missing_sectors(provider: DataProvider | None = None, limit: int | None = None) -> dict:
    """Isi sektor yang masih kosong dari profil Yahoo. Hasilnya aproksimasi."""
    provider = provider or YahooProvider()
    with logged_run("sectors") as res:
        with SessionLocal() as s:
            ids = {c: int(i) for c, i in s.execute(text("SELECT code, id FROM sectors")).all()}
            todo = s.execute(text("""
                SELECT ticker, yahoo_symbol FROM companies
                WHERE is_active AND sector_id IS NULL ORDER BY ticker""")).all()
            for n, (ticker, symbol) in enumerate(todo[:limit] if limit else todo, start=1):
                try:
                    prof = provider.fetch_profile(symbol)
                except Exception:  # noqa: BLE001
                    res["failed"] += 1
                    continue
                code = INDUSTRY_TO_CODE.get(prof.get("industry")) or YAHOO_SECTOR.get(prof.get("sector"))
                if code in ids:
                    s.execute(text("UPDATE companies SET sector_id = :sid, is_financial = :fin WHERE ticker = :t"),
                              {"sid": ids[code], "fin": code == "FIN", "t": ticker})
                    res["rows"] += 1
                if n % 50 == 0:
                    s.commit()
                time.sleep(0.5)
            s.commit()
    return res
```

Tambahan `worker/cli.py` (di samping `seed-rules` dari bagian 14.7):

```python
sub.add_parser("fill-sectors", help="isi sektor kosong dari profil Yahoo (aproksimasi)")
# ...
elif args.cmd == "fill-sectors":
    sync_companies.fill_missing_sectors()
```

**Urutan setup final**

1. `alembic upgrade head`
2. `python -m worker.cli seed` (mengisi `sectors` lalu `companies`)
3. `python -m worker.cli fill-sectors` (hanya bila ada emiten tanpa sektor)
4. `python -m worker.cli seed-rules`
5. `python -m worker.cli backfill --start 2021-01-01`
6. Jalankan job fundamental sekali (bagian 14.7)
7. `python -m worker.main` untuk menyalakan penjadwal

Pemeriksaan cepat setelah langkah 2 sampai 3:

```sql
SELECT count(*) AS total, count(sector_id) AS bersektor FROM companies WHERE is_active;
SELECT s.code, count(*) FROM companies c JOIN sectors s ON s.id = c.sector_id GROUP BY s.code ORDER BY 2 DESC;
```

Catatan: emiten tanpa sektor tetap tampil di peta pasar pada kelompok "Lainnya", tetapi tidak ikut perhitungan Leading Sectors. Mutu sektor hasil `fill-sectors` lebih rendah daripada pemetaan IDX-IC resmi; ganti dengan `sector_map.csv` sebelum rilis publik.

### 14.11 Frontend: Watchlist dan Portfolio

Halaman ini memakai komponen dari bagian 14.6 dan 14.9. Ada beberapa perubahan kecil pada berkas yang sudah ada; lakukan dulu sebelum menambah berkas baru.

**Perubahan pada berkas yang sudah ada**

```ts
// lib/csv.ts: izinkan tipe MIME lain (untuk ekspor JSON)
export function download(name: string, text: string, mime = "text/csv;charset=utf-8") {
  const url = URL.createObjectURL(new Blob([text], { type: mime }));
  // ...sisanya tetap
}
```

```tsx
// components/table/DataTable.tsx
// 1) import:  import type { ReactNode } from "react";
// 2) tambahkan close_vs_high ke PCT dan LABEL:
//      PCT:   "close_vs_high"
//      LABEL: close_vs_high: "Jarak ke High 52W"
// 3) tanda tangan fungsi dan dua sisipan untuk kolom aksi:
export function DataTable({ columns, rows, actions }: {
  columns: string[]; rows: ScreenerRow[]; actions?: (row: ScreenerRow) => ReactNode;
}) {
  // di <tr> header, setelah hg.headers.map(...):   {actions && <th className="px-3 py-2" />}
  // di <tr> baris,  setelah r.getVisibleCells().map(...):
  //                {actions && <td className="px-3 py-1.5">{actions(r.original)}</td>}
}
```

```ts
// store/portfolio.ts: tambah replaceAll ke interface State dan implementasi,
// serta fungsi parseHoldings di bawah valueHolding
//   interface State { ...; replaceAll: (h: Holding[]) => void }
//   implementasi:    replaceAll: (holdings) => set({ holdings }),

export function parseHoldings(text: string): Holding[] {
  const raw = JSON.parse(text);
  if (!Array.isArray(raw)) throw new Error("Format tidak valid: harus berupa daftar");
  return raw.map((x) => {
    if (typeof x?.ticker !== "string" || !(Number(x.lots) > 0) || !(Number(x.avgPrice) > 0)) {
      throw new Error("Ada baris dengan ticker, lot, atau harga rata-rata yang tidak valid");
    }
    return {
      id: crypto.randomUUID(),
      ticker: x.ticker.trim().toUpperCase(),
      lots: Number(x.lots),
      avgPrice: Number(x.avgPrice),
      fee: x.fee ? Number(x.fee) : undefined,
      boughtAt: typeof x.boughtAt === "string" ? x.boughtAt : undefined,
    };
  });
}
```

```tsx
// App.tsx: tambahkan rute
const Watchlist = lazy(() => import("./pages/Watchlist"));
const Portfolio = lazy(() => import("./pages/Portfolio"));
// di dalam <Routes>:
//   <Route path="/watchlist" element={<Navigate to="/watchlist/leading-stocks" replace />} />
//   <Route path="/watchlist/:slug" element={<Watchlist />} />
//   <Route path="/portfolio" element={<Portfolio />} />
// AppShell.tsx: tambahkan ke NAV
//   { to: "/watchlist/leading-stocks", label: "Watchlist" }, { to: "/portfolio", label: "Portfolio" }
```

**Tipe dan hook baru**

```ts
// api/types.ts (tambahan)
export interface WatchlistInfo {
  slug: string; name: string; description: string; rule_expr: string; members?: number;
}
export interface WatchlistRow {
  rank: number; trade_date: string; ticker: string; name: string; sector: string | null;
  close: number; ret_1d: number | null; ret_1m: number | null; rs_rating: number | null;
  close_vs_high: number | null;
}
export interface WatchlistResponse {
  as_of: string | null; watchlist: WatchlistInfo; count: number; data: WatchlistRow[];
}
export interface QuoteRow { ticker: string; close: number; trade_date: string; sector: string | null }
export interface QuoteResponse { data: QuoteRow[] }
```

```ts
// api/hooks.ts (tambahan)
export const useWatchlists = () =>
  useQuery({
    queryKey: ["watchlists"],
    queryFn: () => api<{ data: WatchlistInfo[] }>("/watchlists"),
    staleTime: 5 * 60_000,
  });

export const useWatchlist = (slug: string) =>
  useQuery({
    queryKey: ["watchlist", slug],
    queryFn: () => api<WatchlistResponse>(`/watchlists/${slug}`),
    staleTime: 5 * 60_000,
  });

export function useQuotes(tickers: string[]) {
  const key = [...new Set(tickers)].sort();
  return useQuery({
    queryKey: ["quotes", key],
    queryFn: () =>
      api<QuoteResponse>("/portfolio/quote", { method: "POST", body: JSON.stringify({ tickers: key }) }),
    enabled: key.length > 0,
    staleTime: 5 * 60_000,
  });
}
```

**Pantauan pribadi dan kartu aturan**

```ts
// store/pins.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface PinState { tickers: string[]; toggle: (ticker: string) => void }

export const usePins = create<PinState>()(
  persist(
    (set) => ({
      tickers: [],
      toggle: (t) => set((s) => ({
        tickers: s.tickers.includes(t) ? s.tickers.filter((x) => x !== t) : [...s.tickers, t],
      })),
    }),
    { name: "idxw-pins-v1" },
  ),
);
```

```tsx
// components/common/RuleCard.tsx
interface Props { name: string; description: string; expr: string; count: number; asOf: string | null }

export function RuleCard({ name, description, expr, count, asOf }: Props) {
  return (
    <div className="rounded border border-[--border] bg-[--surface] p-3 text-sm">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="font-semibold">{name}</h1>
        <span className="text-xs text-[--muted]">{count} saham · dihitung {asOf ?? "–"}</span>
      </div>
      <p className="mt-1">{description}</p>
      <details className="mt-2 text-xs">
        <summary className="cursor-pointer text-[--muted]">Ekspresi teknis</summary>
        <code className="mt-1 block whitespace-pre-wrap break-words">{expr}</code>
      </details>
    </div>
  );
}
```

**Halaman Watchlist**

```tsx
// pages/Watchlist.tsx
import { useMemo } from "react";
import { Link, useParams } from "react-router-dom";
import { useWatchlist, useWatchlists } from "../api/hooks";
import type { ScreenerRow } from "../api/types";
import { RuleCard } from "../components/common/RuleCard";
import { DataTable } from "../components/table/DataTable";
import { usePins } from "../store/pins";

const COLUMNS = ["ticker", "name", "sector", "close", "ret_1d", "ret_1m", "rs_rating", "close_vs_high"];

export default function Watchlist() {
  const { slug = "leading-stocks" } = useParams();
  const lists = useWatchlists();
  const { data, isLoading, error, refetch } = useWatchlist(slug);
  const { tickers, toggle } = usePins();

  const rows = useMemo(
    () => (data?.data ?? []).map((r) => ({ ...r, score: null, na_reason: {} }) as ScreenerRow),
    [data],
  );

  return (
    <section className="space-y-3 p-4">
      <nav className="flex gap-2 overflow-x-auto pb-1 text-sm" aria-label="Daftar pantauan">
        {lists.data?.data.map((w) => (
          <Link key={w.slug} to={`/watchlist/${w.slug}`}
            className={`whitespace-nowrap rounded px-3 py-1 ${w.slug === slug ? "bg-[--accent] text-white" : "border border-[--border]"}`}>
            {w.name} <span className="opacity-70">({w.members ?? 0})</span>
          </Link>
        ))}
      </nav>

      {isLoading && <div className="h-48 animate-pulse rounded bg-[--surface]" />}
      {error && <button className="underline" onClick={() => refetch()}>Gagal memuat. Coba lagi</button>}

      {data && (
        <>
          <RuleCard name={data.watchlist.name} description={data.watchlist.description}
            expr={data.watchlist.rule_expr} count={data.count} asOf={data.as_of} />
          {rows.length === 0 ? (
            <p className="text-[--muted]">Tidak ada saham yang memenuhi aturan pada tanggal ini.</p>
          ) : (
            <DataTable columns={COLUMNS} rows={rows}
              actions={(r) => (
                <button onClick={() => toggle(r.ticker)} aria-pressed={tickers.includes(r.ticker)}
                  aria-label={`Pantau ${r.ticker}`} className="text-lg leading-none">
                  {tickers.includes(r.ticker) ? "★" : "☆"}
                </button>
              )} />
          )}
        </>
      )}

      {tickers.length > 0 && (
        <p className="text-xs text-[--muted]">Pantauan pribadi (hanya di peramban ini): {tickers.join(", ")}</p>
      )}
    </section>
  );
}
```

Catatan: Leading Sectors saat ini hanya dipakai di dalam perhitungan Focus List dan belum disimpan sebagai tabel, sehingga belum bisa ditampilkan sebagai daftar sendiri. Untuk menampilkannya, tambahkan tabel `sector_scores` (trade\_date, sector\_id, median return 3 bulan, persentase di atas SMA50, skor, peringkat) lewat migrasi `0002`, tulis dari `leading_sector_ids` di `run_rules.py`, dan sajikan lewat endpoint baru. Ini dicatat sebagai pekerjaan lanjutan MVP.

**Donat alokasi**

```tsx
// components/charts/AllocationDonut.tsx
import { useEffect, useRef } from "react";
import * as echarts from "echarts/core";
import { PieChart } from "echarts/charts";
import { LegendComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import { fmtPct, fmtRp } from "../../lib/format";

echarts.use([PieChart, TooltipComponent, LegendComponent, CanvasRenderer]);

export interface Slice { name: string; value: number }

export function AllocationDonut({ items, label }: { items: Slice[]; label: string }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current);
    const total = items.reduce((s, i) => s + i.value, 0) || 1;
    chart.setOption({
      tooltip: {
        trigger: "item",
        formatter: (p: any) => `${p.name}<br/>${fmtRp(p.value)} · ${fmtPct(p.value / total, 1).replace("+", "")}`,
      },
      legend: { bottom: 0, textStyle: { color: "#8b95a5" } },
      series: [{
        type: "pie", radius: ["50%", "75%"], avoidLabelOverlap: true,
        label: { show: false }, itemStyle: { borderColor: "#0d1117", borderWidth: 1 }, data: items,
      }],
    });
    const ro = new ResizeObserver(() => chart.resize());
    ro.observe(ref.current);
    return () => { ro.disconnect(); chart.dispose(); };
  }, [items]);

  return <div ref={ref} className="h-64 w-full" role="img" aria-label={label} />;
}
```

**Halaman Portfolio**

```tsx
// pages/Portfolio.tsx
import { useMemo, useState, type FormEvent } from "react";
import { useQuotes } from "../api/hooks";
import { AllocationDonut } from "../components/charts/AllocationDonut";
import { download } from "../lib/csv";
import { fmtNum, fmtPct, fmtRp } from "../lib/format";
import { parseHoldings, usePortfolio, valueHolding } from "../store/portfolio";

const EMPTY = { ticker: "", lots: "", avgPrice: "", fee: "" };
const inp = "rounded border border-[--border] bg-[--surface] px-2 py-1 text-sm";
const signed = (v: number) => `${v >= 0 ? "+" : "−"}${fmtRp(Math.abs(v))}`;
const tone = (v: number) => (v >= 0 ? "text-[--up]" : "text-[--down]");

export default function Portfolio() {
  const { holdings, add, remove, clear, replaceAll } = usePortfolio();
  const [form, setForm] = useState(EMPTY);
  const [msg, setMsg] = useState<string | null>(null);
  const quotes = useQuotes(holdings.map((h) => h.ticker));

  const byTicker = useMemo(
    () => new Map((quotes.data?.data ?? []).map((q) => [q.ticker, q])),
    [quotes.data],
  );
  const rows = useMemo(
    () => holdings.map((h) => {
      const q = byTicker.get(h.ticker);
      return { h, q, v: q ? valueHolding(h, q.close) : null };
    }),
    [holdings, byTicker],
  );
  const totals = useMemo(
    () => rows.reduce((a, r) => (r.v ? { cost: a.cost + r.v.cost, value: a.value + r.v.value } : a),
      { cost: 0, value: 0 }),
    [rows],
  );
  const pnl = totals.value - totals.cost;
  const slices = useMemo(() => {
    const m = new Map<string, number>();
    for (const r of rows) if (r.v) m.set(r.q?.sector ?? "Lainnya", (m.get(r.q?.sector ?? "Lainnya") ?? 0) + r.v.value);
    return [...m].map(([name, value]) => ({ name, value }));
  }, [rows]);
  const missing = rows.filter((r) => !r.q).map((r) => r.h.ticker);

  const submit = (e: FormEvent) => {
    e.preventDefault();
    const lots = Number(form.lots), avg = Number(form.avgPrice);
    if (!/^[A-Za-z]{4}$/.test(form.ticker) || !(lots > 0) || !(avg > 0)) {
      setMsg("Ticker harus 4 huruf; lot dan harga rata-rata harus lebih dari 0.");
      return;
    }
    add({ ticker: form.ticker.toUpperCase(), lots, avgPrice: avg, fee: form.fee ? Number(form.fee) : undefined });
    setForm(EMPTY);
    setMsg(null);
  };

  const onImport = async (file: File | undefined) => {
    if (!file) return;
    try {
      replaceAll(parseHoldings(await file.text()));
      setMsg("Portofolio berhasil diimpor.");
    } catch (err) {
      setMsg(err instanceof Error ? err.message : "Berkas tidak dapat dibaca.");
    }
  };

  return (
    <section className="space-y-4 p-4">
      <p className="text-xs text-[--muted]">
        Data portofolio hanya tersimpan di peramban ini. Server hanya menerima daftar ticker untuk mengambil harga.
      </p>

      <form onSubmit={submit} className="flex flex-wrap items-end gap-2">
        <label className="text-xs">Ticker<br /><input className={`${inp} w-24 uppercase`} maxLength={4}
          value={form.ticker} onChange={(e) => setForm({ ...form, ticker: e.target.value })} /></label>
        <label className="text-xs">Lot<br /><input className={`${inp} w-24`} inputMode="decimal"
          value={form.lots} onChange={(e) => setForm({ ...form, lots: e.target.value })} /></label>
        <label className="text-xs">Harga rata-rata (Rp)<br /><input className={`${inp} w-32`} inputMode="decimal"
          value={form.avgPrice} onChange={(e) => setForm({ ...form, avgPrice: e.target.value })} /></label>
        <label className="text-xs">Biaya (Rp, opsional)<br /><input className={`${inp} w-32`} inputMode="decimal"
          value={form.fee} onChange={(e) => setForm({ ...form, fee: e.target.value })} /></label>
        <button className="rounded bg-[--accent] px-3 py-1 text-sm text-white">Tambah</button>
      </form>
      {msg && <p role="status" className="text-sm">{msg}</p>}
      {missing.length > 0 && quotes.isSuccess && (
        <p className="text-sm text-[--down]">Ticker tidak ditemukan dan tidak dihitung: {missing.join(", ")}</p>
      )}

      {holdings.length === 0 ? (
        <p className="text-[--muted]">Belum ada holding. Tambahkan saham pertama Anda di atas.</p>
      ) : (
        <>
          <div className="grid gap-2 sm:grid-cols-3">
            <div className="rounded border border-[--border] bg-[--surface] p-3">
              <div className="text-xs text-[--muted]">Nilai pasar</div>
              <div className="text-lg font-semibold tabular-nums">{fmtRp(totals.value)}</div>
            </div>
            <div className="rounded border border-[--border] bg-[--surface] p-3">
              <div className="text-xs text-[--muted]">Modal</div>
              <div className="text-lg font-semibold tabular-nums">{fmtRp(totals.cost)}</div>
            </div>
            <div className="rounded border border-[--border] bg-[--surface] p-3">
              <div className="text-xs text-[--muted]">Untung/rugi</div>
              <div className={`text-lg font-semibold tabular-nums ${tone(pnl)}`}>
                {signed(pnl)} ({totals.cost ? fmtPct(pnl / totals.cost, 1) : "–"})
              </div>
            </div>
          </div>

          <div className="overflow-x-auto rounded border border-[--border]">
            <table className="w-full text-sm tabular-nums">
              <thead className="bg-[--surface] text-right">
                <tr>
                  <th className="px-3 py-2 text-left">Ticker</th><th className="px-3 py-2">Lot</th>
                  <th className="px-3 py-2">Harga rata-rata</th><th className="px-3 py-2">Harga terakhir</th>
                  <th className="px-3 py-2">Nilai</th><th className="px-3 py-2">Untung/rugi</th><th />
                </tr>
              </thead>
              <tbody>
                {rows.map(({ h, q, v }) => (
                  <tr key={h.id} className="border-t border-[--border] text-right">
                    <td className="px-3 py-1.5 text-left font-medium">{h.ticker}</td>
                    <td className="px-3 py-1.5">{fmtNum(h.lots)}</td>
                    <td className="px-3 py-1.5">{fmtNum(h.avgPrice)}</td>
                    <td className="px-3 py-1.5">{q ? fmtNum(q.close) : "–"}</td>
                    <td className="px-3 py-1.5">{v ? fmtRp(v.value) : "–"}</td>
                    <td className={`px-3 py-1.5 ${v ? tone(v.pnl) : ""}`}>
                      {v ? `${signed(v.pnl)} (${fmtPct(v.pnlPct, 1)})` : "–"}
                    </td>
                    <td className="px-3 py-1.5">
                      <button onClick={() => remove(h.id)} aria-label={`Hapus ${h.ticker}`}>✕</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {slices.length > 0 && <AllocationDonut items={slices} label="Alokasi portofolio per sektor" />}
          {quotes.data?.data[0] && (
            <p className="text-xs text-[--muted]">Harga penutupan per {quotes.data.data[0].trade_date}.</p>
          )}
        </>
      )}

      <div className="flex flex-wrap items-center gap-3 text-sm">
        <button className="underline" disabled={holdings.length === 0}
          onClick={() => download("idx-witcher-portfolio.json", JSON.stringify(holdings, null, 2), "application/json")}>
          Ekspor JSON
        </button>
        <label className="cursor-pointer underline">Impor JSON
          <input type="file" accept="application/json" className="hidden"
            onChange={(e) => onImport(e.target.files?.[0])} /></label>
        <button className="underline" disabled={holdings.length === 0}
          onClick={() => { if (confirm("Hapus seluruh portofolio di peramban ini?")) clear(); }}>
          Hapus semua
        </button>
      </div>
    </section>
  );
}
```

Tes yang disarankan untuk halaman ini: `parseHoldings` (daftar valid, bukan array, baris dengan lot 0), `valueHolding` dengan biaya, dan uji E2E Playwright "tambah holding, muat ulang halaman, holding masih ada" untuk memastikan persistensi `localStorage`.

### 14.12 Leading Sectors (tabel, API, dan halaman)

Bagian ini menutup catatan di 14.11: peringkat sektor disimpan ke tabel `sector_scores`, disajikan lewat `/sectors/leading`, dan tampil sebagai tab di Watchlist.

`backend/alembic/versions/0002_sector_scores.py`

```python
from alembic import op

revision = "0002"
down_revision = "0001"

SQL = """
CREATE TABLE sector_scores (
  trade_date       DATE NOT NULL,
  sector_id        SMALLINT NOT NULL REFERENCES sectors(id),
  members          INTEGER NOT NULL,
  med_ret_3m       REAL,
  pct_above_sma50  REAL,
  score            REAL,
  rank             SMALLINT,
  is_leading       BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (trade_date, sector_id)
);
"""


def upgrade() -> None:
    op.execute(SQL)


def downgrade() -> None:
    op.execute("DROP TABLE sector_scores")
```

Model di `core/models.py`:

```python
class SectorScore(Base):
    __tablename__ = "sector_scores"
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    sector_id: Mapped[int] = mapped_column(ForeignKey("sectors.id"), primary_key=True)
    members: Mapped[int] = mapped_column(Integer)
    med_ret_3m: Mapped[float | None] = _float()
    pct_above_sma50: Mapped[float | None] = _float()
    score: Mapped[float | None] = _float()
    rank: Mapped[int | None] = mapped_column(SmallInteger)
    is_leading: Mapped[bool] = mapped_column(Boolean, default=False)
```

Perubahan `backend/worker/jobs/run_rules.py`. Ganti fungsi `leading_sector_ids` dengan `sector_ranking`, tambahkan `SectorScore` ke impor dari `core.models`, lalu ganti satu baris di `run()`.

```python
def sector_ranking(df: pd.DataFrame, top: int = 3, min_members: int = 5) -> pd.DataFrame:
    """Indeks = sector_id. Kolom: members, med_ret_3m, pct_above_sma50, score, rank, is_leading."""
    liquid = df[(df["value_avg20"] >= 1e9) & df["sector_id"].notna()]
    g = liquid.groupby("sector_id")
    stats = pd.DataFrame({
        "members": g.size(),
        "med_ret_3m": g["ret_3m"].median(),
        "pct_above_sma50": g.apply(lambda x: (x["close"] > x["sma50"]).mean()),
    })
    stats = stats[stats["members"] >= min_members].copy()   # median bermakna hanya bila anggota cukup
    if stats.empty:
        return stats.assign(score=[], rank=[], is_leading=[])
    stats["score"] = (0.6 * stats["med_ret_3m"].rank(pct=True)
                      + 0.4 * stats["pct_above_sma50"].rank(pct=True))
    stats["rank"] = stats["score"].rank(ascending=False, method="first").astype(int)
    stats["is_leading"] = stats["rank"] <= top
    return stats.sort_values("rank")
```

```python
# di run(), ganti:   sector_ids = leading_sector_ids(today)
# dengan:
ranking = sector_ranking(today)
sector_ids = ranking.index[ranking["is_leading"]].astype(int).tolist()
res["rows"] += upsert(s, SectorScore, [
    {"trade_date": day, "sector_id": int(sid), "members": int(r["members"]),
     "med_ret_3m": _f(r["med_ret_3m"]), "pct_above_sma50": _f(r["pct_above_sma50"]),
     "score": _f(r["score"]), "rank": int(r["rank"]), "is_leading": bool(r["is_leading"])}
    for sid, r in ranking.iterrows()], ["trade_date", "sector_id"])
```

`backend/app/routers/sectors.py` (tambahkan `sectors` ke daftar modul di `app/main.py`)

```python
from datetime import date as Date

from fastapi import APIRouter, Query
from sqlalchemy import text

from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["sectors"])


@cached()
def build_leading_sectors(on: str | None) -> dict:
    with SessionLocal() as s:
        rows = s.execute(text("""
            SELECT ss.trade_date, ss.rank, ss.is_leading, ss.members, ss.med_ret_3m,
                   ss.pct_above_sma50, ss.score, sc.code, sc.name
            FROM sector_scores ss JOIN sectors sc ON sc.id = ss.sector_id
            WHERE ss.trade_date = COALESCE(CAST(:d AS date),
                  (SELECT max(trade_date) FROM sector_scores))
            ORDER BY ss.rank"""), {"d": on}).mappings().all()
    return {"as_of": rows[0]["trade_date"] if rows else on, "data": [dict(r) for r in rows]}


@router.get("/sectors/leading")
def leading_sectors(date: Date | None = Query(None)):
    return build_leading_sectors(on=date.isoformat() if date else None)
```

Frontend. Tambahan tipe, hook, dan formatter:

```ts
// api/types.ts
export interface SectorScoreRow {
  rank: number; code: string; name: string; members: number; is_leading: boolean;
  med_ret_3m: number | null; pct_above_sma50: number | null; score: number | null;
}
export interface LeadingSectorsResponse { as_of: string | null; data: SectorScoreRow[] }

// api/hooks.ts
export const useLeadingSectors = () =>
  useQuery({
    queryKey: ["leading-sectors"],
    queryFn: () => api<LeadingSectorsResponse>("/sectors/leading"),
    staleTime: 5 * 60_000,
  });

// lib/format.ts: proporsi tanpa tanda plus
export const fmtShare = (v: number | null | undefined, digits = 0) =>
  v == null ? "–" : `${(v * 100).toLocaleString("id-ID", { minimumFractionDigits: digits, maximumFractionDigits: digits })}%`;
```

`RuleCard` mendapat properti satuan agar kartu sektor tidak menulis "saham" (ubah dua tempat):

```tsx
// components/common/RuleCard.tsx
interface Props { name: string; description: string; expr: string; count: number; asOf: string | null; unit?: string }
export function RuleCard({ name, description, expr, count, asOf, unit = "saham" }: Props) {
  // ...ganti teks ringkasan menjadi:  {count} {unit} · dihitung {asOf ?? "–"}
}
```

`frontend/src/components/common/WatchlistTabs.tsx` (menggantikan blok `<nav>` dan hook `useWatchlists` di `Watchlist.tsx`; hapus impor `Link` dan `useWatchlists` dari berkas itu, lalu tulis `<WatchlistTabs current={slug} />`)

```tsx
import { Link } from "react-router-dom";
import { useWatchlists } from "../../api/hooks";

export function WatchlistTabs({ current }: { current: string }) {
  const lists = useWatchlists();
  const tabs = [
    ...(lists.data?.data.map((w) => ({ slug: w.slug, label: `${w.name} (${w.members ?? 0})` })) ?? []),
    { slug: "leading-sectors", label: "Leading Sectors" },
  ];
  return (
    <nav className="flex gap-2 overflow-x-auto pb-1 text-sm" aria-label="Daftar pantauan">
      {tabs.map((t) => (
        <Link key={t.slug} to={`/watchlist/${t.slug}`}
          className={`whitespace-nowrap rounded px-3 py-1 ${t.slug === current ? "bg-[--accent] text-white" : "border border-[--border]"}`}>
          {t.label}
        </Link>
      ))}
    </nav>
  );
}
```

`frontend/src/pages/LeadingSectors.tsx`

```tsx
import { useLeadingSectors } from "../api/hooks";
import { RuleCard } from "../components/common/RuleCard";
import { WatchlistTabs } from "../components/common/WatchlistTabs";
import { fmtNum, fmtPct, fmtShare } from "../lib/format";

export default function LeadingSectors() {
  const { data, isLoading, error, refetch } = useLeadingSectors();
  return (
    <section className="space-y-3 p-4">
      <WatchlistTabs current="leading-sectors" />
      <RuleCard name="Leading Sectors" unit="sektor memimpin"
        description="Sektor dengan median return 3 bulan dan proporsi saham di atas SMA50 tertinggi. Hanya saham likuid yang dihitung, dan sektor harus punya minimal 5 anggota likuid."
        expr="skor = 0.6 * persentil(median ret_3m) + 0.4 * persentil(% anggota di atas SMA50); 3 peringkat teratas memimpin"
        count={data?.data.filter((r) => r.is_leading).length ?? 0} asOf={data?.as_of ?? null} />
      {isLoading && <div className="h-40 animate-pulse rounded bg-[--surface]" />}
      {error && <button className="underline" onClick={() => refetch()}>Gagal memuat. Coba lagi</button>}
      {data && data.data.length === 0 && <p className="text-[--muted]">Belum ada peringkat sektor.</p>}
      {data && data.data.length > 0 && (
        <div className="overflow-x-auto rounded border border-[--border]">
          <table className="w-full text-sm tabular-nums">
            <thead className="bg-[--surface] text-right">
              <tr>
                <th className="px-3 py-2 text-left">#</th><th className="px-3 py-2 text-left">Sektor</th>
                <th className="px-3 py-2">Anggota likuid</th><th className="px-3 py-2">Median 3M</th>
                <th className="px-3 py-2">Di atas SMA50</th><th className="px-3 py-2">Skor</th>
                <th className="px-3 py-2 text-left">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.data.map((r) => (
                <tr key={r.code} className="border-t border-[--border] text-right">
                  <td className="px-3 py-1.5 text-left">{r.rank}</td>
                  <td className="px-3 py-1.5 text-left font-medium">{r.name}</td>
                  <td className="px-3 py-1.5">{r.members}</td>
                  <td className="px-3 py-1.5">{fmtPct(r.med_ret_3m, 1)}</td>
                  <td className="px-3 py-1.5">{fmtShare(r.pct_above_sma50)}</td>
                  <td className="px-3 py-1.5">{r.score == null ? "–" : fmtNum(r.score * 100)}</td>
                  <td className="px-3 py-1.5 text-left">{r.is_leading ? "Memimpin" : ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
```

Rute: `const LeadingSectors = lazy(() => import("./pages/LeadingSectors"));` dan `<Route path="/watchlist/leading-sectors" element={<LeadingSectors />} />` di `App.tsx`. React Router mengutamakan segmen statis di atas `:slug`, jadi urutan penulisan tidak berpengaruh.

### 14.13 Endpoint dan halaman 17 screen

Screener (bagian 14.5) dan screen berbagi satu loader data `app/frame.py`, yang sekaligus memperbaiki dua hal: kolom yang belum terisi dijadikan angka `NaN` (bukan `None` yang merusak perbandingan), dan `market_cap` selalu dihitung dari harga terbaru, tidak tertimpa snapshot mingguan.

`backend/app/frame.py`

```python
import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal

ALL_COLS = [
    "close", "market_cap", "ret_1d", "ret_1m", "ret_3m", "ret_ytd", "ret_1y", "sma20", "sma50",
    "sma150", "sma200", "hi_52w", "lo_52w", "vol_avg20", "value_avg20", "atr14", "rs_rating",
    "pe_ttm", "pb", "ps", "ev_ebitda", "roe", "roa", "gross_margin", "op_margin", "net_margin",
    "debt_equity", "current_ratio", "div_yield", "payout", "revenue_ttm", "net_income_ttm",
    "fcf_ttm", "rev_growth_yoy", "eps_growth_yoy",
]

SQL = text("""
    SELECT c.ticker, c.name, s.code AS sector, p.close, p.trade_date,
           p.close * c.shares_outstanding AS market_cap,
           to_jsonb(i) - 'ticker' - 'trade_date' AS ind,
           to_jsonb(f) - 'ticker' - 'as_of' AS fun
    FROM companies c
    JOIN prices_daily p ON p.ticker = c.ticker
         AND p.trade_date = (SELECT max(trade_date) FROM indicators_daily)
    LEFT JOIN indicators_daily i ON i.ticker = c.ticker AND i.trade_date = p.trade_date
    LEFT JOIN LATERAL (SELECT * FROM fundamentals_snapshot x WHERE x.ticker = c.ticker
                       ORDER BY as_of DESC LIMIT 1) f ON TRUE
    LEFT JOIN sectors s ON s.id = c.sector_id
    WHERE c.is_active
""")


def load_frame() -> pd.DataFrame:
    """Satu baris per saham aktif pada tanggal data terbaru: harga, indikator, fundamental."""
    with SessionLocal() as s:
        raw = s.execute(SQL).mappings().all()
    records = []
    for r in raw:
        row = {k: (float(v) if hasattr(v, "is_finite") else v)
               for k, v in dict(r).items() if k not in ("ind", "fun")}
        mcap = row.get("market_cap")
        row.update(r["ind"] or {})
        fun = dict(r["fun"] or {})
        row["na_reason"] = fun.pop("na_reason", {}) or {}
        row.update(fun)
        row["market_cap"] = mcap          # harga terbaru x saham beredar, bukan snapshot mingguan
        records.append(row)
    df = pd.DataFrame(records)
    if df.empty:
        return df
    for c in ALL_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df.columns else float("nan")
    return df
```

Perubahan `app/routers/screener.py`: hapus konstanta `SQL` dan blok `with SessionLocal() ... records.append(row)`, impor `from app.frame import load_frame`, lalu ganti bagian awal `build_screener` (dari `spec = menus[menu]` sampai sebelum `as_of = ...`) dengan:

```python
    spec = menus[menu]
    cols = [*spec["columns"], "score", "na_reason"]
    df = load_frame()
    if df.empty:
        return {"as_of": None, "menu": menu, "columns": [*spec["columns"], "score"], "data": []}
```

Baris `needed ... df[col] = None` yang menambah kolom kosong tetap dipertahankan hanya untuk kolom non-numerik; kolom angka sudah dijamin ada oleh `load_frame`.

`backend/rules/screens.yaml` (17 screen dari bagian 10.4)

```yaml
- {slug: murah-menguntungkan, name: Murah dan menguntungkan, description: PER wajar dengan ROE memadai., expr: "0 < pe_ttm <= 15 and roe >= 0.12"}
- {slug: dividen-konsisten, name: Dividen konsisten, description: Imbal dividen tinggi dengan payout tidak berlebihan dan laba positif., expr: "div_yield >= 0.04 and 0 < payout <= 0.8 and net_income_ttm > 0"}
- {slug: utang-rendah, name: Utang rendah, description: Rasio utang terhadap ekuitas kecil dan likuiditas jangka pendek kuat., expr: "debt_equity <= 0.5 and current_ratio >= 1.5"}
- {slug: pertumbuhan-laba, name: Pertumbuhan laba, description: Laba dan pendapatan tumbuh dibanding kuartal sama tahun lalu., expr: "eps_growth_yoy >= 0.2 and rev_growth_yoy >= 0.1"}
- {slug: margin-tinggi, name: Margin tinggi, description: Margin bersih dan operasi tinggi., expr: "net_margin >= 0.15 and op_margin >= 0.2"}
- {slug: di-bawah-nilai-buku, name: Di bawah nilai buku, description: PBV di bawah 1 dengan ROE positif., expr: "0 < pb < 1 and roe > 0"}
- {slug: arus-kas-kuat, name: Arus kas kuat, description: Arus kas bebas positif dan setidaknya 80% dari laba bersih., expr: "fcf_ttm > 0 and fcf_ttm >= 0.8 * net_income_ttm"}
- {slug: kualitas, name: Kualitas, description: ROE dan margin baik dengan utang terkendali., expr: "roe >= 0.15 and net_margin >= 0.1 and debt_equity <= 1"}
- {slug: small-cap-likuid, name: Small cap likuid, description: Market cap Rp500 miliar sampai Rp5 triliun dengan transaksi harian memadai., expr: "5e11 <= market_cap <= 5e12 and value_avg20 >= 1e9"}
- {slug: big-cap-defensif, name: Big cap defensif, description: Market cap besar dengan imbal dividen tinggi., expr: "market_cap >= 5e13 and div_yield >= 0.03"}
- {slug: momentum-kuat, name: Momentum kuat, description: Naik 20% atau lebih dalam 3 bulan dan di atas SMA50., expr: "ret_3m >= 0.2 and close > sma50"}
- {slug: dekat-high-52w, name: Dekat high 52 minggu, description: Harga dalam 5% dari puncak 52 minggu., expr: "close >= 0.95 * hi_52w"}
- {slug: dekat-low-52w, name: Dekat low 52 minggu, description: Harga dalam 10% dari dasar 52 minggu., expr: "close <= 1.10 * lo_52w"}
- {slug: terkoreksi-di-tren-naik, name: Terkoreksi di tren naik, description: Turun 10% atau lebih dalam sebulan tetapi masih di atas SMA200., expr: "close > sma200 and ret_1m <= -0.10"}
- {slug: likuiditas-tinggi, name: Likuiditas tinggi, description: Nilai transaksi harian rata-rata minimal Rp50 miliar., expr: "value_avg20 >= 5e10"}
- {slug: pertumbuhan-wajar, name: Pertumbuhan wajar, description: Pertumbuhan laba baik dengan PER tidak berlebihan., expr: "0 < pe_ttm <= 25 and eps_growth_yoy >= 0.15"}
- {slug: laba-membaik, name: Laba membaik, description: Laba positif dan melonjak dibanding kuartal sama tahun lalu., expr: "net_income_ttm > 0 and eps_growth_yoy >= 0.5"}
```

`backend/app/routers/screens.py` (daftarkan di `app/main.py`)

```python
from fastapi import APIRouter

from app.errors import ApiError
from app.frame import load_frame
from core.cache import cached
from core.rules import apply_rule, load_rules

router = APIRouter(tags=["screens"])
COLS = ["ticker", "name", "sector", "market_cap", "close", "pe_ttm", "pb", "roe",
        "div_yield", "ret_3m", "rs_rating"]


def _hit(df, expr: str):
    return apply_rule(df, " ".join(expr.split()))


@cached()
def build_screens() -> dict:
    df = load_frame()
    out = []
    for r in load_rules("screens"):
        out.append({"slug": r["slug"], "name": r["name"], "description": r["description"],
                    "expr": r["expr"], "members": 0 if df.empty else len(_hit(df, r["expr"]))})
    return {"as_of": None if df.empty else df["trade_date"].iloc[0], "data": out}


@cached()
def build_screen(slug: str) -> dict:
    spec = next((r for r in load_rules("screens") if r["slug"] == slug), None)
    if spec is None:
        raise ApiError(404, "not_found", f"Screen '{slug}' tidak ada")
    info = {k: spec[k] for k in ("slug", "name", "description", "expr")}
    df = load_frame()
    if df.empty:
        return {"as_of": None, "screen": info, "columns": COLS, "count": 0, "data": []}
    hit = _hit(df, spec["expr"]).sort_values("market_cap", ascending=False, na_position="last")
    cols = [*COLS, "na_reason"]
    data = hit[cols].astype(object).where(hit[cols].notna(), None).to_dict("records")
    for row in data:
        row["score"] = None
    return {"as_of": df["trade_date"].iloc[0], "screen": info, "columns": COLS,
            "count": len(data), "data": data}


@router.get("/screens")
def screens():
    return build_screens()


@router.get("/screens/{slug}")
def screen(slug: str):
    return build_screen(slug=slug)
```

Tes tambahan di `tests/test_rules.py`:

```python
from app.frame import ALL_COLS


def test_every_screen_expression_parses_and_there_are_17():
    df = pd.DataFrame([[1.0] * len(ALL_COLS)], columns=ALL_COLS)
    rules = load_rules("screens")
    assert len(rules) == 17
    for r in rules:
        apply_rule(df, " ".join(r["expr"].split()))
```

Frontend: tipe, hook, dan halaman.

```ts
// api/types.ts
export interface ScreenInfo { slug: string; name: string; description: string; expr: string; members?: number }
export interface ScreensResponse { as_of: string | null; data: ScreenInfo[] }
export interface ScreenResponse {
  as_of: string | null; screen: ScreenInfo; columns: string[]; count: number; data: ScreenerRow[];
}

// api/hooks.ts
export const useScreens = () =>
  useQuery({ queryKey: ["screens"], queryFn: () => api<ScreensResponse>("/screens"), staleTime: 5 * 60_000 });

export const useScreen = (slug: string) =>
  useQuery({ queryKey: ["screen", slug], queryFn: () => api<ScreenResponse>(`/screens/${slug}`), staleTime: 5 * 60_000 });
```

```tsx
// pages/Screens.tsx
import { Link, useParams } from "react-router-dom";
import { useScreen, useScreens } from "../api/hooks";
import { RuleCard } from "../components/common/RuleCard";
import { DataTable } from "../components/table/DataTable";

function ScreenList() {
  const { data, isLoading, error } = useScreens();
  return (
    <section className="space-y-3 p-4">
      <h1 className="font-semibold">Screens</h1>
      <p className="text-sm text-[--muted]">Filter berbasis aturan. Setiap kartu menampilkan aturannya.</p>
      {isLoading && <div className="h-40 animate-pulse rounded bg-[--surface]" />}
      {error && <p>Gagal memuat screens.</p>}
      <ul className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {data?.data.map((s) => (
          <li key={s.slug}>
            <Link to={`/screens/${s.slug}`} className="block rounded border border-[--border] bg-[--surface] p-3 text-sm hover:border-[--accent]">
              <div className="flex items-baseline justify-between">
                <span className="font-medium">{s.name}</span>
                <span className="text-xs text-[--muted]">{s.members ?? 0} saham</span>
              </div>
              <p className="mt-1 text-xs text-[--muted]">{s.description}</p>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

function ScreenDetail({ slug }: { slug: string }) {
  const { data, isLoading, error, refetch } = useScreen(slug);
  return (
    <section className="space-y-3 p-4">
      <Link to="/screens" className="text-sm underline">← Semua screens</Link>
      {isLoading && <div className="h-40 animate-pulse rounded bg-[--surface]" />}
      {error && <button className="underline" onClick={() => refetch()}>Gagal memuat. Coba lagi</button>}
      {data && (
        <>
          <RuleCard name={data.screen.name} description={data.screen.description}
            expr={data.screen.expr} count={data.count} asOf={data.as_of} />
          {data.data.length === 0
            ? <p className="text-[--muted]">Tidak ada saham yang memenuhi aturan ini.</p>
            : <DataTable columns={data.columns} rows={data.data} />}
        </>
      )}
    </section>
  );
}

export default function Screens() {
  const { slug } = useParams();
  return slug ? <ScreenDetail slug={slug} /> : <ScreenList />;
}
```

Rute dan navigasi: tambahkan `const Screens = lazy(() => import("./pages/Screens"));`, `<Route path="/screens" element={<Screens />} />` dan `<Route path="/screens/:slug" element={<Screens />} />` di `App.tsx`, serta `{ to: "/screens", label: "Screens" }` ke `NAV` di `AppShell.tsx`.

### 14.14 Frontend: halaman Stock dan Start Here

Pasang grafik versi 4: `npm i lightweight-charts@4`. Kode di bawah memakai API v4 (`addCandlestickSeries`); versi 5 mengganti API ini dengan `addSeries`, jadi jangan memasang versi terbaru tanpa menyesuaikan kode.

**Utilitas baru**

```ts
// lib/indicators.ts
export function sma(bars: { time: string; close: number }[], n: number) {
  const out: { time: string; value: number }[] = [];
  let sum = 0;
  for (let i = 0; i < bars.length; i++) {
    sum += bars[i].close;
    if (i >= n) sum -= bars[i - n].close;
    if (i >= n - 1) out.push({ time: bars[i].time, value: sum / n });
  }
  return out;
}
```

```ts
// lib/indicators.test.ts
import { expect, it } from "vitest";
import { sma } from "./indicators";

it("menghitung SMA 2 periode", () => {
  const bars = [1, 2, 3, 4].map((c, i) => ({ time: `2026-01-0${i + 1}`, close: c }));
  expect(sma(bars, 2).map((p) => p.value)).toEqual([1.5, 2.5, 3.5]);
});
```

```ts
// lib/metrics.ts: pindahkan PCT, RP, dan LABEL dari DataTable.tsx ke sini, lalu impor di DataTable
import { fmtNum, fmtPct, fmtRp } from "./format";

export const PCT = new Set(["ret_1d", "ret_1m", "ret_3m", "ret_ytd", "ret_1y", "roe", "roa", "gross_margin",
  "op_margin", "net_margin", "div_yield", "payout", "rev_growth_yoy", "eps_growth_yoy", "close_vs_high"]);
export const RP = new Set(["market_cap", "revenue_ttm", "net_income_ttm", "fcf_ttm", "value_avg20"]);
export const LABEL: Record<string, string> = {
  ticker: "Ticker", name: "Nama", sector: "Sektor", market_cap: "Market cap", close: "Harga",
  pe_ttm: "PER", pb: "PBV", ps: "PSR", ev_ebitda: "EV/EBITDA", div_yield: "Dividen",
  roe: "ROE", roa: "ROA", gross_margin: "Margin kotor", op_margin: "Margin operasi",
  net_margin: "Margin bersih", debt_equity: "DER", current_ratio: "Current ratio", payout: "Payout",
  rev_growth_yoy: "Pertumbuhan pendapatan", eps_growth_yoy: "Pertumbuhan laba",
  revenue_ttm: "Pendapatan TTM", net_income_ttm: "Laba bersih TTM", fcf_ttm: "FCF TTM",
  ret_1d: "1D", ret_1m: "1M", ret_3m: "3M", ret_ytd: "YTD", ret_1y: "1Y", rs_rating: "RS",
  sma50: "SMA50", sma200: "SMA200", hi_52w: "High 52W", lo_52w: "Low 52W",
  value_avg20: "Nilai transaksi 20D", vol_avg20: "Volume 20D", close_vs_high: "Jarak ke High 52W",
  score: "Skor",
};

export function fmtMetric(col: string, v: number): string {
  return PCT.has(col) ? fmtPct(v, 1) : RP.has(col) ? fmtRp(v) : fmtNum(v);
}
```

```ts
// lib/signals.ts: label sinyal yang dipakai Feed dan Stock (pindahkan konstanta KIND dari Feed.tsx)
export const SIGNAL_LABEL: Record<string, string> = {
  new_high: "High 52 minggu baru", new_low: "Low 52 minggu baru",
  volume_surge: "Lonjakan volume", big_move: "Pergerakan besar",
  breakdown_sma50: "Turun di bawah SMA50", breakout_sma50: "Naik di atas SMA50",
  breakdown_sma200: "Turun di bawah SMA200", breakout_sma200: "Naik di atas SMA200",
};
```

**Tipe dan hook**

```ts
// api/types.ts
export interface PriceBar {
  time: string; open: number; high: number; low: number; close: number; volume: number | null;
}
export interface PricesResponse { ticker: string; range: string; data: PriceBar[] }
export interface StockResponse {
  as_of: string; ticker: string; name: string; sector: string | null; close: number;
  indicators: Record<string, number | null>;
  fundamentals: Record<string, number | null>;
  na_reason: Record<string, NaReasonKey>;
  signals: { trade_date: string; kind: string; detail: Record<string, number | null> }[];
}

// api/hooks.ts
export const useStock = (ticker: string) =>
  useQuery({
    queryKey: ["stock", ticker],
    queryFn: () => api<StockResponse>(`/stocks/${ticker}`),
    staleTime: 5 * 60_000,
    retry: false,
  });

export const useStockPrices = (ticker: string) =>
  useQuery({
    queryKey: ["prices", ticker],
    queryFn: () => api<PricesResponse>(`/stocks/${ticker}/prices?range=5y`),
    staleTime: 5 * 60_000,
  });
```

Seluruh riwayat 5 tahun diunduh sekali; tombol rentang hanya mengubah jendela yang terlihat, sehingga SMA200 tetap benar pada rentang pendek.

**Grafik harga**

```tsx
// components/charts/PriceChart.tsx
import { useEffect, useRef } from "react";
import { createChart, type Time } from "lightweight-charts";
import type { PriceBar } from "../../api/types";
import { sma } from "../../lib/indicators";

const UP = "#22c55e";
const DOWN = "#f87171";

export function PriceChart({ bars, days }: { bars: PriceBar[]; days: number | null }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el || bars.length === 0) return;
    const chart = createChart(el, {
      height: 360,
      layout: { background: { color: "transparent" }, textColor: "#8b95a5" },
      grid: { vertLines: { visible: false }, horzLines: { color: "rgba(139,149,165,0.15)" } },
      rightPriceScale: { borderVisible: false },
      timeScale: { borderVisible: false },
    });
    const candles = chart.addCandlestickSeries({
      upColor: UP, downColor: DOWN, borderVisible: false, wickUpColor: UP, wickDownColor: DOWN,
    });
    candles.setData(bars.map((b) => ({
      time: b.time as Time, open: b.open, high: b.high, low: b.low, close: b.close,
    })));
    for (const [n, color] of [[20, "#60a5fa"], [50, "#f59e0b"], [200, "#a78bfa"]] as const) {
      const line = chart.addLineSeries({ color, lineWidth: 1, priceLineVisible: false, lastValueVisible: false });
      line.setData(sma(bars, n).map((p) => ({ time: p.time as Time, value: p.value })));
    }
    const vol = chart.addHistogramSeries({ priceFormat: { type: "volume" }, priceScaleId: "" });
    vol.priceScale().applyOptions({ scaleMargins: { top: 0.85, bottom: 0 } });
    vol.setData(bars.map((b) => ({
      time: b.time as Time, value: b.volume ?? 0,
      color: b.close >= b.open ? "rgba(34,197,94,0.35)" : "rgba(248,113,113,0.35)",
    })));
    const last = bars[bars.length - 1].time;
    if (days) {
      const from = new Date(Date.parse(last) - days * 864e5).toISOString().slice(0, 10);
      chart.timeScale().setVisibleRange({ from: from as Time, to: last as Time });
    } else {
      chart.timeScale().fitContent();
    }
    const ro = new ResizeObserver(() => chart.applyOptions({ width: el.clientWidth }));
    ro.observe(el);
    return () => { ro.disconnect(); chart.remove(); };
  }, [bars, days]);

  return <div ref={ref} className="w-full" role="img" aria-label="Grafik harga dengan SMA20, SMA50, dan SMA200" />;
}
```

**Halaman Stock**

```tsx
// pages/Stock.tsx
import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ApiError } from "../api/client";
import { useStock, useStockPrices } from "../api/hooks";
import type { NaReasonKey } from "../api/types";
import { PriceChart } from "../components/charts/PriceChart";
import { NaCell } from "../components/table/NaCell";
import { fmtNum, fmtPct } from "../lib/format";
import { fmtMetric, LABEL } from "../lib/metrics";
import { SIGNAL_LABEL } from "../lib/signals";

const RANGES: [string, number | null][] = [["1M", 31], ["3M", 93], ["1Y", 366], ["5Y", 1830], ["Max", null]];
const TECH = ["ret_1d", "ret_1m", "ret_3m", "ret_ytd", "ret_1y", "rs_rating", "sma50", "sma200",
  "hi_52w", "lo_52w", "value_avg20"];
const FUND = ["pe_ttm", "pb", "ps", "ev_ebitda", "roe", "roa", "net_margin", "debt_equity",
  "current_ratio", "div_yield", "rev_growth_yoy", "eps_growth_yoy"];

function Metrics({ title, cols, values, na }: {
  title: string; cols: string[]; values: Record<string, number | null>; na: Record<string, NaReasonKey>;
}) {
  return (
    <div className="rounded border border-[--border] bg-[--surface] p-3">
      <h2 className="mb-2 text-sm font-semibold">{title}</h2>
      <dl className="grid grid-cols-1 gap-y-1 text-sm sm:grid-cols-2">
        {cols.map((c) => (
          <div key={c} className="flex justify-between gap-4 sm:pr-4">
            <dt className="text-[--muted]">{LABEL[c] ?? c}</dt>
            <dd className="tabular-nums">
              {values[c] == null ? <NaCell reason={na[c]} /> : fmtMetric(c, values[c] as number)}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

export default function Stock() {
  const { ticker = "" } = useParams();
  const code = ticker.toUpperCase();
  const [days, setDays] = useState<number | null>(366);
  const stock = useStock(code);
  const prices = useStockPrices(code);

  if (stock.error instanceof ApiError && stock.error.status === 404) {
    return <p className="p-4">Ticker {code} tidak ditemukan. <Link className="underline" to="/">Kembali ke Explore</Link></p>;
  }
  if (stock.isLoading) return <div className="m-4 h-64 animate-pulse rounded bg-[--surface]" />;
  if (!stock.data) return <p className="p-4">Gagal memuat data saham.</p>;

  const s = stock.data;
  const day = s.indicators.ret_1d;
  return (
    <section className="space-y-4 p-4">
      <header className="flex flex-wrap items-baseline gap-x-4 gap-y-1">
        <h1 className="text-xl font-semibold">{s.ticker}</h1>
        <span className="text-[--muted]">{s.name}{s.sector ? ` · ${s.sector}` : ""}</span>
        <span className="ml-auto text-lg tabular-nums">
          {fmtNum(s.close)}{" "}
          {day != null && <span className={day >= 0 ? "text-[--up]" : "text-[--down]"}>{fmtPct(day)}</span>}
        </span>
      </header>

      <div className="flex gap-2">
        {RANGES.map(([label, d]) => (
          <button key={label} onClick={() => setDays(d)}
            className={`rounded px-3 py-1 text-sm ${days === d ? "bg-[--accent] text-white" : "border border-[--border]"}`}>
            {label}
          </button>
        ))}
      </div>
      {prices.isLoading && <div className="h-[360px] animate-pulse rounded bg-[--surface]" />}
      {prices.data && <PriceChart bars={prices.data.data} days={days} />}
      <p className="text-xs text-[--muted]">SMA20 biru, SMA50 oranye, SMA200 ungu. Harga penutupan per {s.as_of}.</p>

      <div className="grid gap-3 lg:grid-cols-2">
        <Metrics title="Teknikal" cols={TECH} values={s.indicators} na={s.na_reason} />
        <Metrics title="Fundamental (TTM)" cols={FUND} values={s.fundamentals} na={s.na_reason} />
      </div>

      <div>
        <h2 className="mb-2 text-sm font-semibold">Sinyal terbaru</h2>
        {s.signals.length === 0 ? (
          <p className="text-sm text-[--muted]">Belum ada sinyal untuk saham ini.</p>
        ) : (
          <ul className="space-y-1 text-sm">
            {s.signals.map((g) => (
              <li key={`${g.trade_date}-${g.kind}`} className="flex gap-3">
                <span className="tabular-nums text-[--muted]">{g.trade_date}</span>
                <span>{SIGNAL_LABEL[g.kind] ?? g.kind}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
```

**Halaman Start Here**

Aturan pada halaman ini diambil langsung dari API sehingga selalu sama dengan yang dijalankan sistem.

```tsx
// pages/Start.tsx
import type { ReactNode } from "react";
import { useScreens, useWatchlists } from "../api/hooks";

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="space-y-2">
      <h2 className="text-base font-semibold">{title}</h2>
      {children}
    </section>
  );
}

function Rule({ name, description, expr }: { name: string; description: string; expr: string }) {
  return (
    <details className="rounded border border-[--border] bg-[--surface] p-3 text-sm">
      <summary className="cursor-pointer font-medium">{name}</summary>
      <p className="mt-1 text-[--muted]">{description}</p>
      <code className="mt-1 block whitespace-pre-wrap break-words text-xs">{expr}</code>
    </details>
  );
}

export default function Start() {
  const lists = useWatchlists();
  const screens = useScreens();
  return (
    <article className="mx-auto max-w-3xl space-y-6 p-4 text-sm leading-relaxed">
      <h1 className="text-xl font-semibold">Start Here</h1>

      <Section title="Apa itu IDX Witcher">
        <p>Alat riset untuk saham Bursa Efek Indonesia: peta pasar, daftar pantauan berbasis aturan, screener,
          portofolio pribadi, dan feed perubahan harian. Setiap daftar menampilkan aturannya, dan setiap sel kosong
          menampilkan alasannya.</p>
      </Section>

      <Section title="Sumber data dan jadwal">
        <ul className="list-disc space-y-1 pl-5">
          <li>Harga dan fundamental berasal dari Yahoo Finance melalui pustaka tidak resmi, sehingga dapat terlambat, hilang, atau keliru.</li>
          <li>Data bersifat end-of-day: diperbarui sekali sehari sekitar pukul 17:00 WIB pada hari bursa. Tanggal data terlihat di footer.</li>
          <li>Fundamental diperbarui mingguan dan mengikuti laporan keuangan yang tersedia di sumber.</li>
        </ul>
      </Section>

      <Section title="Cara membaca angka">
        <ul className="list-disc space-y-1 pl-5">
          <li><b>bank</b>: rasio tidak berlaku untuk bank, asuransi, dan perusahaan pembiayaan.</li>
          <li><b>no data</b>: tidak ada laporan keuangan di sumber data.</li>
          <li><b>loss</b>: laba 12 bulan terakhir negatif, sehingga rasio tidak bermakna.</li>
          <li><b>n/a</b>: tidak dilaporkan atau dibuang oleh pemeriksaan kualitas data (misalnya PER di atas 1.000).</li>
          <li>TTM = jumlah 4 kuartal terakhir. Pertumbuhan pendapatan dan laba dibandingkan dengan kuartal yang sama tahun lalu, bukan TTM.</li>
          <li>Market cap = harga penutupan × jumlah saham beredar. Nilai transaksi = harga × volume (aproksimasi).</li>
          <li>Satuan rupiah: T = triliun, M = miliar, Jt = juta. 1 lot = 100 lembar.</li>
        </ul>
      </Section>

      <Section title="Indikator">
        <ul className="list-disc space-y-1 pl-5">
          <li>Return 1D, 1M, 3M, 1Y dihitung dari harga penutupan 1, 21, 63, dan 252 sesi sebelumnya; YTD terhadap penutupan terakhir tahun lalu.</li>
          <li>SMA = rata-rata harga penutupan 20, 50, 150, atau 200 sesi. High/Low 52W = penutupan tertinggi/terendah 252 sesi.</li>
          <li>RS Rating (1 sampai 99) = peringkat persentil kekuatan harga relatif, dengan bobot terbesar pada 3 bulan terakhir, di antara saham likuid.</li>
          <li>Likuid = nilai transaksi rata-rata 20 sesi minimal Rp1 miliar.</li>
        </ul>
      </Section>

      <Section title="Aturan daftar pantauan">
        {lists.data?.data.map((w) => <Rule key={w.slug} name={w.name} description={w.description} expr={w.rule_expr} />)}
      </Section>

      <Section title="Aturan screens">
        {screens.data?.data.map((s) => <Rule key={s.slug} name={s.name} description={s.description} expr={s.expr} />)}
      </Section>

      <Section title="Keterbatasan">
        <ul className="list-disc space-y-1 pl-5">
          <li>Indikator memakai harga penutupan tanpa penyesuaian split atau rights, sehingga saham yang baru mengalaminya dapat memberi sinyal palsu.</li>
          <li>Sektor mengikuti klasifikasi yang dimuat sistem dan dapat berbeda dari klasifikasi resmi bursa.</li>
          <li>Saham yang disuspensi atau jarang diperdagangkan dapat menampilkan harga basi.</li>
          <li>Tidak ada data real-time atau intraday.</li>
        </ul>
      </Section>

      <Section title="Disclaimer">
        <p>IDX Witcher adalah alat riset dan edukasi. Hasil daftar dan screen adalah filter mekanis berdasarkan
          aturan di atas, bukan rekomendasi untuk membeli atau menjual efek apa pun. Keputusan investasi adalah
          tanggung jawab Anda; pertimbangkan berkonsultasi dengan penasihat keuangan berlisensi.</p>
      </Section>
    </article>
  );
}
```

**Perubahan pada berkas yang sudah ada**

```tsx
// App.tsx: tambahkan rute
const Stock = lazy(() => import("./pages/Stock"));
const Start = lazy(() => import("./pages/Start"));
//   <Route path="/stock/:ticker" element={<Stock />} />
//   <Route path="/start" element={<Start />} />

// AppShell.tsx: tambahkan { to: "/start", label: "Start Here" } ke NAV, dan ubah footer menjadi:
//   ... Bukan saran investasi. Grafik: TradingView Lightweight Charts. <Link to="/start">Metodologi</Link>

// pages/Explore.tsx: klik kotak peta membuka halaman saham
//   import { useNavigate } from "react-router-dom";
//   const navigate = useNavigate();   // ganti useState selected
//   <MarketMap rows={data.data} onSelect={(t) => navigate(`/stock/${t}`)} />

// components/table/DataTable.tsx: ticker menjadi tautan, dan PCT/RP/LABEL diimpor dari lib/metrics
//   import { Link } from "react-router-dom";
//   import { LABEL, PCT, RP } from "../../lib/metrics";
//   di renderCell, baris pertama:
//   if (col === "ticker") return <Link className="text-[--accent]" to={`/stock/${String(row.ticker)}`}>{String(row.ticker)}</Link>;
```

**Daftar periksa integrasi (setelah semua bagian terpasang)**

1. `pytest -q` di `backend` hijau (indikator, kualitas, aturan watchlist dan screen).
2. `npx vitest run` dan `npm run build` di `frontend` hijau.
3. `docker compose up -d --build`, lalu jalankan urutan setup final dari bagian 14.10.
4. Buka `/api/docs`: semua endpoint tercantum dan `/api/v1/meta` menampilkan `as_of` terbaru.
5. Di web: Explore terisi, klik kotak membuka `/stock/<ticker>` dengan grafik; Screener dan Screens menampilkan sel abu-abu beralasan; Watchlist dan tab Leading Sectors terisi; Feed menampilkan sinyal; Portfolio bertahan setelah muat ulang.
6. Matikan jaringan pada worker lalu jalankan pipeline: status `failed` tercatat di `ingest_runs`, alert terkirim, dan web tetap menampilkan data hari sebelumnya.

### 14.15 Menu screener lengkap, migrasi awal, dan konfigurasi Alembic

Bagian ini menutup tiga celah setup: `menus.yaml` dengan 14 menu, migrasi `0001`, dan berkas konfigurasi Alembic.

`backend/rules/menus.yaml` (menggantikan contoh dua menu di bagian 14.5; kunci menu sama dengan id di `Screener.tsx`)

```yaml
overview:
  columns: [ticker, name, sector, market_cap, close, ret_1d, pe_ttm, pb, div_yield, rs_rating]
  higher: [rs_rating, div_yield]
  lower: [pe_ttm, pb]
valuation:
  columns: [ticker, name, sector, market_cap, close, pe_ttm, pb, ps, ev_ebitda, div_yield]
  higher: [div_yield]
  lower: [pe_ttm, pb, ps, ev_ebitda]
profitability:
  columns: [ticker, name, sector, market_cap, close, roe, roa, gross_margin, op_margin, net_margin]
  higher: [roe, roa, gross_margin, op_margin, net_margin]
  lower: []
growth:
  columns: [ticker, name, sector, market_cap, close, rev_growth_yoy, eps_growth_yoy, revenue_ttm, net_income_ttm]
  higher: [rev_growth_yoy, eps_growth_yoy, net_income_ttm]
  lower: []
dividends:
  columns: [ticker, name, sector, market_cap, close, div_yield, payout, net_income_ttm, pe_ttm]
  higher: [div_yield, net_income_ttm]
  lower: [pe_ttm]
balance-sheet:
  columns: [ticker, name, sector, market_cap, close, debt_equity, current_ratio, roe]
  higher: [current_ratio, roe]
  lower: [debt_equity]
cash-flow:
  columns: [ticker, name, sector, market_cap, close, fcf_ttm, revenue_ttm, net_income_ttm]
  higher: [fcf_ttm, revenue_ttm, net_income_ttm]
  lower: []
quality:
  columns: [ticker, name, sector, market_cap, close, roe, roa, net_margin, debt_equity, current_ratio]
  higher: [roe, roa, net_margin, current_ratio]
  lower: [debt_equity]
efficiency:
  columns: [ticker, name, sector, market_cap, close, roe, roa, op_margin]
  higher: [roe, roa, op_margin]
  lower: []
momentum:
  columns: [ticker, name, sector, market_cap, close, ret_1m, ret_3m, ret_ytd, ret_1y, rs_rating]
  higher: [ret_1m, ret_3m, ret_ytd, ret_1y, rs_rating]
  lower: []
technical:
  columns: [ticker, name, sector, market_cap, close, ret_1d, sma50, sma200, hi_52w, lo_52w]
  higher: []
  lower: []
liquidity:
  columns: [ticker, name, sector, market_cap, close, value_avg20, vol_avg20]
  higher: []
  lower: []
size:
  columns: [ticker, name, sector, market_cap, close, revenue_ttm, net_income_ttm]
  higher: []
  lower: []
ownership:            # Fase 2: kolom kepemilikan menyusul setelah impor berkas ≥1%
  columns: [ticker, name, sector, market_cap, close]
  higher: []
  lower: []
```

Tes untuk menjaga konsistensi (`tests/test_menus.py`):

```python
from app.frame import ALL_COLS
from core.rules import load_rules

TEXT = {"ticker", "name", "sector"}
FRONTEND_IDS = {"overview", "valuation", "profitability", "growth", "dividends", "balance-sheet",
                "cash-flow", "quality", "efficiency", "momentum", "technical", "liquidity",
                "size", "ownership"}


def test_menus_match_frontend_and_known_columns():
    menus = load_rules("menus")
    assert set(menus) == FRONTEND_IDS
    for name, spec in menus.items():
        for col in spec["columns"]:
            assert col in ALL_COLS or col in TEXT, f"{name}: kolom tidak dikenal {col}"
        for col in [*spec["higher"], *spec["lower"]]:
            assert col in ALL_COLS, f"{name}: metrik skor tidak dikenal {col}"
```

`backend/alembic.ini`

```ini
[alembic]
script_location = alembic
prepend_sys_path = .

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

`backend/alembic/env.py` (URL database diambil dari pengaturan aplikasi, bukan dari `alembic.ini`)

```python
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import core.models  # noqa: F401  (mendaftarkan semua tabel ke metadata)
from core.config import get_settings
from core.db import Base

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url.replace("%", "%%"))
if config.config_file_name:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata,
                      literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

`backend/alembic/versions/0001_init.py` (skema bagian 8; setiap pernyataan dijalankan terpisah agar aman di semua driver)

```python
from alembic import op

revision = "0001"
down_revision = None

SQL = """
CREATE TABLE sectors (
  id    SMALLINT PRIMARY KEY,
  code  TEXT NOT NULL UNIQUE,
  name  TEXT NOT NULL
);

CREATE TABLE companies (
  ticker             TEXT PRIMARY KEY,
  yahoo_symbol       TEXT NOT NULL UNIQUE,
  name               TEXT NOT NULL,
  sector_id          SMALLINT REFERENCES sectors(id),
  subsector          TEXT,
  board              TEXT,
  listing_date       DATE,
  shares_outstanding BIGINT,
  is_financial       BOOLEAN NOT NULL DEFAULT FALSE,
  is_active          BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE prices_daily (
  ticker       TEXT NOT NULL REFERENCES companies(ticker),
  trade_date   DATE NOT NULL,
  open         NUMERIC(18,4),
  high         NUMERIC(18,4),
  low          NUMERIC(18,4),
  close        NUMERIC(18,4) NOT NULL,
  adj_close    NUMERIC(18,4),
  volume       BIGINT,
  value_traded NUMERIC(24,2),
  is_suspect   BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (ticker, trade_date)
);

CREATE INDEX ix_prices_date ON prices_daily (trade_date);

CREATE TABLE corporate_actions (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  action_date DATE NOT NULL,
  kind        TEXT NOT NULL CHECK (kind IN ('dividend','split')),
  value       NUMERIC(18,6) NOT NULL,
  PRIMARY KEY (ticker, action_date, kind)
);

CREATE TABLE financial_statements (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  period_end  DATE NOT NULL,
  period_type TEXT NOT NULL CHECK (period_type IN ('Q','FY')),
  statement   TEXT NOT NULL CHECK (statement IN ('IS','BS','CF')),
  item        TEXT NOT NULL,
  value       NUMERIC(28,2),
  currency    TEXT NOT NULL DEFAULT 'IDR',
  source      TEXT NOT NULL DEFAULT 'yfinance',
  PRIMARY KEY (ticker, period_end, period_type, statement, item)
);

CREATE TABLE indicators_daily (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  trade_date  DATE NOT NULL,
  ret_1d REAL, ret_1m REAL, ret_3m REAL, ret_ytd REAL, ret_1y REAL,
  sma20 REAL, sma50 REAL, sma150 REAL, sma200 REAL,
  hi_52w REAL, lo_52w REAL,
  vol_avg20   DOUBLE PRECISION,
  value_avg20 DOUBLE PRECISION,
  atr14       REAL,
  rs_rating   SMALLINT,
  PRIMARY KEY (ticker, trade_date)
);

CREATE TABLE fundamentals_snapshot (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  as_of       DATE NOT NULL,
  market_cap  NUMERIC(28,2),
  pe_ttm REAL, pb REAL, ps REAL, ev_ebitda REAL,
  roe REAL, roa REAL, gross_margin REAL, op_margin REAL, net_margin REAL,
  debt_equity REAL, current_ratio REAL,
  div_yield REAL, payout REAL,
  revenue_ttm NUMERIC(28,2), net_income_ttm NUMERIC(28,2), fcf_ttm NUMERIC(28,2),
  rev_growth_yoy REAL, eps_growth_yoy REAL,
  na_reason   JSONB NOT NULL DEFAULT '{}'::jsonb,
  PRIMARY KEY (ticker, as_of)
);

CREATE TABLE watchlists (
  slug        TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  description TEXT NOT NULL,
  rule_expr   TEXT NOT NULL,
  sort_order  SMALLINT NOT NULL DEFAULT 0
);

CREATE TABLE watchlist_members (
  slug        TEXT NOT NULL REFERENCES watchlists(slug),
  trade_date  DATE NOT NULL,
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  rank        INTEGER,
  PRIMARY KEY (slug, trade_date, ticker)
);

CREATE TABLE signals (
  id          BIGSERIAL PRIMARY KEY,
  trade_date  DATE NOT NULL,
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  kind        TEXT NOT NULL,
  detail      JSONB NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (trade_date, ticker, kind)
);

CREATE INDEX ix_signals_date ON signals (trade_date DESC);

CREATE TABLE holder_groups (id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);

CREATE TABLE holders (
  id               SERIAL PRIMARY KEY,
  name             TEXT NOT NULL,
  name_normalized  TEXT NOT NULL UNIQUE,
  kind             TEXT,
  group_id         INTEGER REFERENCES holder_groups(id),
  is_public_figure BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE holdings (
  ticker       TEXT NOT NULL REFERENCES companies(ticker),
  holder_id    INTEGER NOT NULL REFERENCES holders(id),
  report_month DATE NOT NULL,
  shares       BIGINT NOT NULL,
  pct          NUMERIC(7,4) NOT NULL,
  PRIMARY KEY (ticker, holder_id, report_month)
);

CREATE TABLE ingest_runs (
  id             BIGSERIAL PRIMARY KEY,
  job            TEXT NOT NULL,
  started_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at    TIMESTAMPTZ,
  status         TEXT NOT NULL DEFAULT 'running',
  rows_written   INTEGER,
  tickers_failed INTEGER,
  error          TEXT
);

CREATE TABLE users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  pw_hash    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""

TABLES = [
    "users", "ingest_runs", "holdings", "holders", "holder_groups", "signals", "watchlist_members",
    "watchlists", "fundamentals_snapshot", "indicators_daily", "financial_statements",
    "corporate_actions", "prices_daily", "companies", "sectors",
]


def upgrade() -> None:
    for stmt in (s.strip() for s in SQL.split(";")):
        if stmt:
            op.execute(stmt)


def downgrade() -> None:
    for table in TABLES:
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
```

Catatan penting:

- Skrip memisahkan pernyataan dengan titik koma, jadi jangan menambahkan titik koma di dalam komentar atau string literal pada `SQL`. Jika Anda memperluas skema, tambahkan migrasi baru (`0003_*.py`) daripada mengubah `0001`.
- `0002` (tabel `sector_scores`, bagian 14.12) bergantung pada `sectors`, jadi urutannya harus `0001` lalu `0002`; `alembic upgrade head` menjalankan keduanya.
- Skrip kini cocok dengan model SQLAlchemy di `core/models.py`. Bila Anda menambah kolom di salah satunya, ubah keduanya, karena model tidak membuat tabel (migrasi yang membuatnya).
- Pemeriksaan: `alembic upgrade head` lalu `psql -c "\dt"` harus menampilkan 16 tabel (15 dari skema ditambah `sector_scores`) dan `alembic_version`.

## 15. Persyaratan Non-Fungsional

Yang paling menentukan kepercayaan pengguna adalah ketepatan data, kecepatan halaman, dan kejelasan bahwa produk ini alat riset, bukan penasihat investasi.

### Performa dan keandalan

| ID | Persyaratan | Target |
| --- | --- | --- |
| NFR-01 | LCP halaman Explore (p75, 4G) | < 2,5 detik |
| NFR-02 | Latensi API baca dari cache / tanpa cache (p95) | < 100 ms / < 400 ms |
| NFR-03 | Pipeline harian selesai sejak dipicu | < 60 menit |
| NFR-04 | Ketersediaan web (bulanan) | ≥ 99% |
| NFR-05 | Backup database | Harian, simpan 14 hari, uji pemulihan tiap kuartal |
| NFR-06 | Kegagalan sumber data | Web tetap tampil dengan data hari sebelumnya dan label `as_of` yang jujur |

### Keamanan

1. **Injeksi SQL**: semua query memakai parameter terikat; f-string hanya untuk nama kolom dari daftar putih (contoh `PERIOD_COL`).
2. **Aturan dari YAML**: ekspresi `pandas.query` hanya berasal dari berkas repo yang ditinjau lewat pull request, tidak pernah dari input pengguna atau parameter API.
3. **Rahasia**: hanya di environment/secret manager; `.env` masuk `.gitignore`; rotasi bila bocor.
4. **Transport dan header**: HTTPS wajib, HSTS, `Content-Security-Policy` ketat, `X-Content-Type-Options: nosniff`.
5. **Batas laju dan CORS**: sesuai bagian 11; basis data tidak dapat diakses langsung dari internet.
6. **Dependensi**: pindai berkala dengan `pip-audit` dan `npm audit` di CI; perbarui lewat Dependabot.
7. **Akun (Fase 2)**: hash kata sandi argon2, cookie `HttpOnly` + `SameSite=Lax`, verifikasi email, batasi percobaan login.

### Privasi

- MVP tidak mengumpulkan data pribadi; portofolio hanya di peramban dan endpoint `/portfolio/quote` menerima daftar ticker saja.
- Analitik penggunaan memakai alat tanpa cookie dan tanpa identitas pribadi (mis. Plausible atau Umami yang di-host sendiri).
- Fase 2 (akun): sediakan hapus akun dan ekspor data; sesuaikan dengan UU Pelindungan Data Pribadi (UU No. 27 Tahun 2022). Konfirmasikan kewajiban rinci dengan penasihat hukum.

### Hukum dan kepatuhan

1. **Bukan saran investasi**: disclaimer tetap di footer semua halaman dan di Start Here. Hindari bahasa yang menyuruh membeli atau menjual ("beli sekarang"); gunakan bahasa deskriptif ("memenuhi aturan X"). Bila produk akan dimonetisasi atau menyasar publik luas, periksa ketentuan OJK tentang penasihat investasi dengan penasihat hukum.
2. **Lisensi data**: data pasar memiliki syarat penggunaan. Yahoo Finance membatasi penggunaan komersial dan redistribusi; data bursa dapat memerlukan lisensi untuk ditampilkan ulang. Sebelum peluncuran publik, pastikan hak tampil dan redistribusi, atau ganti sumber lewat `DataProvider`.
3. **Atribusi**: tampilkan sumber data dan waktu pembaruan di footer; lightweight-charts mewajibkan atribusi sesuai lisensinya.
4. **Lisensi pustaka**: periksa lisensi komponen spreadsheet (Fase 2) sebelum dipakai untuk penggunaan komersial.

### Observabilitas

- Log terstruktur (JSON) di API dan worker; level INFO untuk pipeline, ERROR memicu alert.
- Metrik minimum: durasi tiap job, baris tertulis, ticker gagal, latensi dan status HTTP API.
- Halaman status internal membaca `/meta` (status run terakhir) dan memberi tanda merah bila data lebih tua dari 1 hari bursa.

### Aksesibilitas dan internasionalisasi

- Target WCAG 2.1 AA: kontras, fokus keyboard, label ARIA pada grafik, alternatif tabel untuk peta.
- UI berbahasa Indonesia; teks disimpan di satu berkas string agar bahasa Inggris dapat ditambahkan kemudian.

## 16. Strategi Testing dan QA

Tes difokuskan pada tiga hal yang paling mungkin merusak kepercayaan: rumus indikator yang salah, aturan yang berubah diam-diam, dan data sumber yang rusak.

### Lapisan tes

| Lapisan | Alat | Cakupan | Dijalankan |
| --- | --- | --- | --- |
| Unit Python | pytest | Indikator, aturan, validasi kualitas, formatter | Tiap commit (CI) |
| Integrasi | pytest + Postgres/Redis (service CI) | Upsert idempoten, query API, migrasi Alembic | Tiap pull request |
| Kontrak API | pytest + TestClient | Bentuk JSON, kode error, parameter wajib | Tiap pull request |
| Unit frontend | Vitest | `fmtRp`, `fmtPct`, `valueHolding`, `buildTree` | Tiap commit |
| E2E | Playwright | Explore termuat, filter screener, tambah holding | Sebelum rilis |
| Kualitas data | Pemeriksaan di pipeline | Kelengkapan dan kewajaran hasil harian | Tiap run |

### Contoh tes inti

`backend/tests/test_indicators.py`

```python
import pandas as pd

from worker.indicators import compute_indicators


def _prices(n=300, ticker="AAAA", start=1000.0, step=1.0):
    dates = pd.bdate_range("2025-01-01", periods=n).date
    close = [start + step * i for i in range(n)]
    return pd.DataFrame({
        "ticker": ticker, "date": dates,
        "high": [c * 1.01 for c in close], "low": [c * 0.99 for c in close],
        "close": close, "volume": 1_000_000.0,
        "value_traded": [c * 1_000_000 for c in close],
    })


def test_sma_and_return_match_hand_calculation():
    df = compute_indicators(_prices())
    last = df.iloc[-1]
    assert abs(last["sma20"] - df["close"].tail(20).mean()) < 1e-9
    assert abs(last["ret_1d"] - (1299 / 1298 - 1)) < 1e-9


def test_faster_stock_gets_higher_rs_rating():
    both = pd.concat([_prices(ticker="AAAA", step=1.0), _prices(ticker="BBBB", step=3.0)])
    df = compute_indicators(both)
    last = df[df["date"] == df["date"].max()].set_index("ticker")
    assert last.loc["BBBB", "rs_rating"] > last.loc["AAAA", "rs_rating"]
```

`backend/tests/test_quality.py`

```python
import pandas as pd

from worker.quality import flag_suspect


def test_flags_bad_range_and_large_jump():
    df = pd.DataFrame({
        "ticker": ["AAAA"] * 3,
        "date": pd.to_datetime(["2026-09-28", "2026-09-29", "2026-09-30"]).date,
        "open": [100, 100, 100], "high": [101, 101, 160],
        "low": [99, 105, 99], "close": [100, 100, 150],
    })
    flags = flag_suspect(df).tolist()
    assert flags == [False, True, True]   # low > close, lalu lonjakan 50%
```

`backend/tests/test_rules.py`

```python
import pandas as pd

from core.rules import apply_rule, load_rules


def test_every_watchlist_expression_parses():
    cols = ["close", "sma20", "sma50", "sma150", "sma200", "sma200_20d_ago", "rs_rating",
            "value_avg20", "hi_52w", "hi_20d_prev", "volume", "vol_avg20", "atr14_pct",
            "atr14_pct_20d_ago", "sector_id", "in_leading_stocks"]
    df = pd.DataFrame([[1.0] * len(cols)], columns=cols).astype({"in_leading_stocks": bool})
    for r in load_rules("watchlists"):
        apply_rule(df, r["expr"], leading_sector_ids=[1])   # tidak boleh melempar error
```

`frontend/src/lib/format.test.ts`

```ts
import { describe, expect, it } from "vitest";
import { fmtPct, fmtRp } from "./format";
import { valueHolding } from "../store/portfolio";

describe("format", () => {
  it("menyingkat rupiah", () => expect(fmtRp(1.5e12)).toBe("Rp1,5 T"));
  it("memformat persen", () => expect(fmtPct(0.0123)).toBe("+1,23%"));
});

describe("portfolio", () => {
  it("menghitung untung/rugi 10 lot", () => {
    const r = valueHolding({ id: "1", ticker: "AAAA", lots: 10, avgPrice: 1000 }, 1100);
    expect(r.shares).toBe(1000);
    expect(r.pnl).toBe(100_000);
    expect(r.pnlPct).toBeCloseTo(0.1);
  });
});
```

### Pemeriksaan kualitas data otomatis (akhir tiap run)

1. Jumlah saham bertanggal hari ini ≥ 95% dari jumlah saham aktif kemarin.
2. Tidak ada saham likuid dengan `close` kosong pada tanggal terbaru.
3. Total market cap seluruh saham berubah wajar dibanding kemarin (peringatan bila selisih melebihi ±5%, kira-kira sebanding dengan pergerakan IHSG satu hari yang ekstrem).
4. Setiap daftar watchlist memiliki jumlah anggota dalam rentang historis wajar; nol anggota pada daftar yang biasanya berisi puluhan memicu peringatan.
5. Hasil pemeriksaan ditulis ke `ingest_runs` dan, bila gagal, dikirim ke alert.

### Matriks penerimaan MVP

| Kriteria penerimaan | Dibuktikan oleh |
| --- | --- |
| 5.1 semua saham tampil di peta | Tes kontrak `/market-map` + pemeriksaan kualitas no. 1 |
| 5.2 aturan tampil dan dapat diubah lewat YAML | `test_rules.py` + tes E2E membuka kartu aturan |
| 5.3 tidak ada sel kosong tanpa alasan | Tes kontrak `/screener` (setiap `null` punya `na_reason`) |
| 5.5 hitung portofolio akurat | Vitest `valueHolding` (5 kasus hitung tangan) |
| 5.6 hanya 5 sesi terakhir | Tes kontrak `/feed` |
| NFR-01 sampai NFR-02 | Lighthouse CI dan uji beban ringan (k6/locust) sebelum rilis |

## 17. DevOps, Deployment, dan Biaya

MVP cukup berjalan di satu server Linux kecil dengan Docker Compose; frontend dapat dihosting statis di CDN gratis. Semua lingkungan (lokal, CI, produksi) memakai image dan konfigurasi yang sama.

### `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: iw
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-iw}
      POSTGRES_DB: idxwitcher
    volumes: ["pgdata:/var/lib/postgresql/data"]
    ports: ["5432:5432"]          # hapus baris ini di produksi
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U iw -d idxwitcher"]
      interval: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 10

  migrate:
    build: ./backend
    command: alembic upgrade head
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
    restart: "no"

  api:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    env_file: .env
    depends_on:
      migrate: { condition: service_completed_successfully }
      redis: { condition: service_healthy }
    ports: ["8000:8000"]
    restart: unless-stopped

  worker:
    build: ./backend
    command: python -m worker.main
    env_file: .env
    depends_on:
      migrate: { condition: service_completed_successfully }
      redis: { condition: service_healthy }
    restart: unless-stopped

volumes:
  pgdata:
```

### `backend/Dockerfile`

```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=Asia/Jakarta
WORKDIR /app
COPY pyproject.toml ./
COPY core ./core
COPY providers ./providers
COPY worker ./worker
COPY app ./app
COPY rules ./rules
COPY data ./data
COPY alembic ./alembic
COPY alembic.ini ./
# editable agar core/rules.py menemukan folder rules/ di /app
RUN pip install --no-cache-dir -e .
```

### `.env.example`

```bash
POSTGRES_PASSWORD=ganti-dengan-sandi-kuat
DATABASE_URL=postgresql+psycopg://iw:ganti-dengan-sandi-kuat@db:5432/idxwitcher
REDIS_URL=redis://redis:6379/0
CORS_ORIGINS=["http://localhost:5173"]
PIPELINE_HOUR=17
ALERT_WEBHOOK_URL=
```

### `Makefile` (baris perintah diawali karakter Tab)

```make
.PHONY: up seed backfill test
up:
	docker compose up -d --build
seed:
	docker compose run --rm api python -m worker.cli seed
backfill:
	docker compose run --rm api python -m worker.cli backfill --start 2021-01-01
test:
	cd backend && pytest -q
	cd frontend && npx vitest run
```

### CI: `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_USER: iw, POSTGRES_PASSWORD: iw, POSTGRES_DB: idxwitcher }
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U iw" --health-interval 5s --health-retries 10
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]
    env:
      DATABASE_URL: postgresql+psycopg://iw:iw@localhost:5432/idxwitcher
      REDIS_URL: redis://localhost:6379/0
    defaults: { run: { working-directory: backend } }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: alembic upgrade head
      - run: pytest -q
  frontend:
    runs-on: ubuntu-latest
    defaults: { run: { working-directory: frontend } }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm, cache-dependency-path: frontend/package-lock.json }
      - run: npm ci
      - run: npx vitest run
      - run: npm run build
```

### Opsi deployment

| Opsi | Backend dan database | Frontend | Cocok untuk |
| --- | --- | --- | --- |
| A. Satu VPS | Docker Compose di VPS Linux (2 vCPU dan 2 GB RAM cukup untuk MVP, perkiraan) dengan Caddy sebagai reverse proxy HTTPS | Statis di VPS yang sama atau CDN | Paling murah dan sederhana |
| B. PaaS | Railway, Render, atau Fly.io untuk API + worker; Postgres terkelola | Vercel atau Cloudflare Pages | Sedikit urusan server |
| C. Hibrida tanpa server worker | Pipeline dijalankan GitHub Actions terjadwal menulis ke Postgres terkelola; API di PaaS | Cloudflare Pages | Menghindari worker yang selalu hidup; batasi durasi job |

Contoh `Caddyfile` untuk opsi A (frontend hasil `npm run build` dimount ke `/srv/web`):

```text
iw.contoh.id {
  handle /api/* { reverse_proxy api:8000 }
  handle { root * /srv/web
           try_files {path} /index.html
           file_server }
}
```

### Monitoring dan pemeliharaan

1. Pantau `/api/v1/health` dengan Uptime Kuma atau UptimeRobot; alert ke Telegram/email.
2. `pg_dump` harian ke penyimpanan objek terpisah; uji pemulihan tiap kuartal.
3. Log lewat `docker compose logs`; tambahkan Sentry (opsional) untuk galat API dan frontend.
4. Perbarui dependensi bulanan lewat Dependabot; jalankan ulang tes sebelum deploy.

### Perkiraan biaya bulanan (kasar, cek harga terkini)

| Komponen | Perkiraan | Catatan |
| --- | --- | --- |
| VPS kecil (opsi A) | US$5 sampai 12 | Menjalankan API, worker, Postgres, Redis |
| Postgres terkelola (opsi B/C) | US$0 sampai 25 | Tergantung ukuran dan penyedia |
| Hosting frontend | US$0 | Tingkat gratis CDN statis cukup untuk MVP |
| Domain | sekitar US$10 sampai 15 per tahun | - |
| Data pasar | US$0 di MVP (yfinance) | Sumber berlisensi berbayar bila diluncurkan publik/komersial |

## 18. Roadmap, Risiko, dan Checklist Build

MVP dapat selesai dalam 8 minggu oleh satu developer full-stack dengan dua gerbang yang mencegah kerja sia-sia: data harus bersih sebelum indikator dibangun, dan kontrak API dibekukan sebelum frontend selesai.

&#91;embedded content: roadmap MVP · 8 minggu, 2 gerbang\]

Tanggal mengasumsikan mulai Senin 5 Oktober 2026 dan kerja penuh waktu; dua minggu terakhir frontend berjalan paralel dengan tes dan deploy.

### Fase sesudah MVP (perkiraan)

| Fase | Isi | Durasi perkiraan |
| --- | --- | --- |
| Fase 2 | 1% Screener (impor berkas bulanan), Company Models (xlsx lalu editor), akun dan sinkron portofolio | 6 sampai 8 minggu |
| Fase 3 | Alert Telegram/email, PWA, sumber data berlisensi, backtest sederhana untuk aturan watchlist | 6 sampai 10 minggu |

### Risiko dan mitigasi

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| `yfinance` berubah atau diblokir | Pipeline gagal, data basi | Antarmuka `DataProvider`, simpan data mentah, alert, siapkan penyedia cadangan |
| Data IDX di Yahoo tidak lengkap atau salah | Angka menyesatkan | Sanity check bagian 6, tampilkan `n/a` dan alasannya, bandingkan sampel dengan sumber bursa |
| Hak tampil dan redistribusi data belum jelas | Risiko hukum saat rilis publik | Pastikan lisensi sebelum peluncuran; ganti sumber bila perlu |
| Aksi korporasi (split, rights) mengganggu return dan SMA | Sinyal palsu | Kode awal memakai `close` tanpa penyesuaian: terapkan `adj_close` atau faktor dari `corporate_actions` sebelum rilis publik |
| Saham suspensi atau tidak likuid mencemari daftar | Daftar tidak berguna | Filter nilai transaksi rata-rata 20 sesi dan tanda `is_suspect` |
| Cakupan fitur melebar | MVP terlambat | Prioritas MoSCoW; potong fitur Should bila jadwal tergelincir |
| Pengguna mengira hasil adalah rekomendasi | Risiko reputasi dan hukum | Disclaimer tetap, bahasa deskriptif, halaman Start Here |
| Penarikan data massal lewat API | Beban server | Batas laju dan cache (bagian 11) |

### Checklist build dari nol

- [ ] Buat repo dan struktur folder bagian 13; commit `pyproject.toml`, `docker-compose.yml`, `.env.example`
- [ ] Jalankan `docker compose up db redis`; buat migrasi awal dari skema bagian 8 dan `alembic upgrade head`
- [ ] Siapkan `data/companies_seed.csv` dan `data/sector_map.csv` (11 sektor IDX-IC); jalankan `worker.cli seed`
- [ ] Implementasikan `DataProvider` dan `YahooProvider`; uji dengan 5 ticker
- [ ] Implementasikan `ingest_prices` dan `flag_suspect`; jalankan backfill 2021 sampai sekarang
- [ ] Gerbang 1: pemeriksaan kualitas data lulus pada 30 hari terakhir
- [ ] Implementasikan `indicators.py` dan tes unit dengan hitung tangan
- [ ] Tulis `watchlists.yaml`, `run_rules`, dan isi tabel `watchlists` dari YAML
- [ ] Implementasikan job fundamental, `na_reason`, dan `menus.yaml` (14 menu)
- [ ] Bangun API: `/market-map`, `/screener`, `/watchlists`, `/feed`, `/stocks`, `/portfolio/quote`
- [ ] Gerbang 2: bekukan kontrak API (skema OpenAPI disimpan di `docs/`)
- [ ] Bangun halaman Explore, Screener, Watchlist, Feed, Portfolio, Stock, Start
- [ ] Pasang cache Redis, batas laju, CORS, dan header keamanan
- [ ] Tulis halaman Start Here (metodologi, sumber, disclaimer) dan footer `as_of`
- [ ] Jalankan CI hijau, tes E2E, Lighthouse, dan uji pemulihan backup
- [ ] Deploy (opsi A atau B), nyalakan penjadwal, pantau pipeline tiga hari bursa berturut-turut
- [ ] Tinjau lisensi data dan disclaimer sebelum membagikan tautan ke publik

### 5.4 1% Screener (Fase 2)

**Tujuan**: menampilkan pemegang saham dengan porsi di atas 1% dan perubahannya.

**Tab**: Home, Float Screener, Changes, All stocks, All investors, Conglomerates, Public figures.

- **All stocks / All investors**: tabel per saham (daftar pemegang ≥1%) dan per investor (daftar saham yang dipegang).
- **Float Screener**: estimasi free float per saham = 100% dikurangi total porsi pemegang tetap (pengendali, pemerintah, afiliasi) yang tercatat. Ini estimasi; tampilkan label "estimasi".
- **Changes**: selisih porsi dan jumlah saham dibandingkan bulan sebelumnya (naik, turun, baru masuk, keluar).
- **Conglomerates**: pemegang dikelompokkan ke grup (mis. satu keluarga/holding) memakai tabel pemetaan manual `holder_groups`.
- **Public figures**: penanda manual untuk investor yang dikenal publik, dikurasi tim (bukan hasil tebakan otomatis).

**Sumber**: berkas kepemilikan bulanan yang dipublikasikan bursa/KSEI. Format dan lokasi berkas dapat berubah; verifikasi sebelum membangun parser dan sediakan jalur impor CSV/XLSX manual.

**AC**: (1) pencarian ticker atau nama investor mengembalikan hasil di bawah 300 ms; (2) setiap baris menampilkan bulan laporan; (3) nama investor dinormalisasi agar variasi penulisan menyatu.

### 5.5 Portfolio

**Tujuan**: memantau nilai dan untung/rugi holding pengguna.

- Input: ticker, jumlah lot (1 lot = 100 lembar), harga rata-rata beli, tanggal beli (opsional), biaya broker (opsional, bisa diatur pengguna).
- Output: nilai pasar = lot × 100 × harga penutupan terakhir; untung/rugi = nilai pasar − modal (rupiah dan persen); alokasi per sektor (donat) dan per saham.
- Penyimpanan: `localStorage`/IndexedDB di peramban (sesuai model "tersimpan di peramban ini saja"); ekspor/impor JSON. Sinkron ke server hanya bila pengguna login (Fase 2).

**AC**: (1) hasil hitung cocok dengan perhitungan manual pada 5 kasus uji; (2) tidak ada data portofolio yang dikirim ke server pada mode lokal.

### 5.6 Daily Feed

**Tujuan**: menjawab "apa yang berubah dalam 5 sesi terakhir".

| Jenis sinyal | Definisi ringkas |
| --- | --- |
| New high / new low | Penutupan tertinggi/terendah 52 minggu (252 sesi) |
| Trend break | Penutupan melintasi SMA50 atau SMA200 dari atas ke bawah (atau sebaliknya) |
| Volume surge | Volume ≥ 2× rata-rata 20 sesi dan nilai transaksi ≥ Rp1 miliar |
| Big move | Perubahan harian absolut ≥ 7% pada saham likuid |
| Dividend | Tanggal cum/ex dividen jatuh dalam jendela 5 sesi |

Feed dikelompokkan per tanggal, dapat difilter per jenis sinyal dan per sektor.

**AC**: (1) hanya sinyal 5 sesi terakhir yang tampil; (2) satu saham dapat muncul di beberapa jenis sinyal; (3) tiap kartu menampilkan nilai pemicu (mis. "volume 3,4× rata-rata").

### 5.7 Company Models (Fase 2)

**Tujuan**: model kuartalan lima emiten terbesar tiap sektor dari laporan keuangan resmi.

- Setiap sel historis dapat ditelusuri ke laporan asal; sel asumsi berwarna hijau menggerakkan proyeksi (pertumbuhan pendapatan, margin, capex, pajak).
- Fase 2a: hasilkan file `.xlsx` dengan rumus (openpyxl) dan sediakan unduhan. Fase 2b: tampilkan spreadsheet interaktif di peramban memakai pustaka spreadsheet (periksa lisensi; opsi: Univer atau Handsontable).

**AC**: (1) mengubah asumsi memperbarui EPS proyeksi; (2) total aset = total liabilitas + ekuitas pada seluruh periode historis.

### 5.8 Start Here dan halaman detail saham

- **Start Here**: halaman statis berisi penjelasan aturan, definisi kolom, sumber data, jadwal pembaruan, keterbatasan data, dan disclaimer.
- **Detail saham** (`/stock/BBCA`): grafik harga dengan SMA20/50/200, ringkasan fundamental, daftar sinyal terbaru, dan pemegang ≥1% bila tersedia.

### 5.9 Akun pengguna (Fase 2)

Pendaftaran email + kata sandi (hash argon2) atau Google OAuth; sinkron portofolio dan pantauan pribadi; hapus akun dan ekspor data sesuai UU Pelindungan Data Pribadi.

### 14.2 Provider data, ingest harga, dan validasi

`backend/providers/base.py`

```python
from abc import ABC, abstractmethod

import pandas as pd


class DataProvider(ABC):
    """Satu-satunya pintu ke sumber data luar. Ganti implementasi tanpa menyentuh kode lain."""

    @abstractmethod
    def fetch_prices(self, symbols: list[str], start: str, end: str | None = None) -> pd.DataFrame:
        """Kolom: symbol, date, open, high, low, close, adj_close, volume.
        Simbol yang gagal diunduh dicatat di df.attrs['failed']."""

    @abstractmethod
    def fetch_actions(self, symbols: list[str]) -> pd.DataFrame:
        """Kolom: symbol, date, kind ('dividend'|'split'), value."""

    @abstractmethod
    def fetch_fundamentals(self, symbol: str) -> dict:
        """Kunci: info (dict), income, balance, cashflow (DataFrame kuartalan)."""
```

`backend/providers/yahoo.py`

```python
import random
import time

import pandas as pd
import yfinance as yf

from core.config import get_settings
from providers.base import DataProvider

COLS = {"Open": "open", "High": "high", "Low": "low", "Close": "close",
        "Adj Close": "adj_close", "Volume": "volume"}


def _retry(fn, attempts: int = 3, base: float = 2.0):
    for i in range(attempts):
        try:
            return fn()
        except Exception:
            if i == attempts - 1:
                raise
            time.sleep(base ** (i + 1) + random.random())


class YahooProvider(DataProvider):
    def fetch_prices(self, symbols, start, end=None):
        cfg = get_settings()
        frames: list[pd.DataFrame] = []
        failed: list[str] = []
        for i in range(0, len(symbols), cfg.yahoo_batch_size):
            batch = symbols[i : i + cfg.yahoo_batch_size]
            try:
                raw = _retry(lambda: yf.download(
                    batch, start=start, end=end, auto_adjust=False,
                    group_by="ticker", threads=True, progress=False))
            except Exception:
                failed.extend(batch)
                continue
            level0 = raw.columns.get_level_values(0) if isinstance(raw.columns, pd.MultiIndex) else []
            for sym in batch:
                if sym not in level0:
                    failed.append(sym)
                    continue
                df = raw[sym].dropna(how="all")
                if df.empty:
                    failed.append(sym)
                    continue
                df = df.rename(columns=COLS).reset_index()
                df = df.rename(columns={df.columns[0]: "date"})
                df["symbol"] = sym
                df["date"] = pd.to_datetime(df["date"]).dt.date
                frames.append(df[["symbol", "date", *COLS.values()]])
            time.sleep(cfg.yahoo_batch_sleep)
        out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
            columns=["symbol", "date", *COLS.values()])
        out.attrs["failed"] = failed
        return out

    def fetch_actions(self, symbols):
        rows = []
        for sym in symbols:
            try:
                act = _retry(lambda: yf.Ticker(sym).actions)
            except Exception:
                continue
            for ts, r in act.iterrows():
                if r.get("Dividends", 0) > 0:
                    rows.append((sym, ts.date(), "dividend", float(r["Dividends"])))
                if r.get("Stock Splits", 0) > 0:
                    rows.append((sym, ts.date(), "split", float(r["Stock Splits"])))
            time.sleep(0.3)
        return pd.DataFrame(rows, columns=["symbol", "date", "kind", "value"])

    def fetch_fundamentals(self, symbol):
        t = yf.Ticker(symbol)
        return {
            "info": _retry(lambda: t.info) or {},
            "income": t.quarterly_income_stmt,
            "balance": t.quarterly_balance_sheet,
            "cashflow": t.quarterly_cashflow,
        }
```

`backend/worker/quality.py`

```python
import pandas as pd

MAX_DAILY_MOVE = 0.35   # di atas ini dianggap mencurigakan (longgar; lihat bagian 6)


def flag_suspect(df: pd.DataFrame) -> pd.Series:
    """df: kolom ticker, date, open, high, low, close. Mengembalikan Series boolean."""
    bad_price = (df[["open", "high", "low", "close"]] <= 0).any(axis=1)
    bad_range = (df["low"] > df["close"]) | (df["close"] > df["high"])
    prev = df.sort_values(["ticker", "date"]).groupby("ticker")["close"].shift()
    jump = (df["close"] / prev - 1).abs() > MAX_DAILY_MOVE
    return (bad_price | bad_range | jump.fillna(False)).astype(bool)
```

`backend/worker/runlog.py` (tambahkan ke pohon folder)

```python
from contextlib import contextmanager
from datetime import datetime, timezone

from core.db import SessionLocal
from core.models import IngestRun


@contextmanager
def logged_run(job: str):
    """Mencatat awal/akhir job di ingest_runs. Yang dikembalikan: dict hasil yang diisi job."""
    result: dict = {"status": "ok", "rows": 0, "failed": 0, "error": None}
    with SessionLocal() as s:
        run = IngestRun(job=job)
        s.add(run)
        s.commit()
        try:
            yield result
        except Exception as exc:  # noqa: BLE001
            result.update(status="failed", error=str(exc)[:500])
        run.status = result["status"]
        run.rows_written = result["rows"]
        run.tickers_failed = result["failed"]
        run.error = result["error"]
        run.finished_at = datetime.now(timezone.utc)
        s.commit()
```

`backend/worker/jobs/ingest_prices.py`

```python
from datetime import date, timedelta

import pandas as pd
from sqlalchemy import select

from core.db import SessionLocal, upsert
from core.models import Company, PriceDaily
from providers.base import DataProvider
from providers.yahoo import YahooProvider
from worker.quality import flag_suspect
from worker.runlog import logged_run

FAIL_TOLERANCE = 0.05


def run(provider: DataProvider | None = None, lookback_days: int = 10,
        start: str | None = None) -> dict:
    provider = provider or YahooProvider()
    start = start or (date.today() - timedelta(days=lookback_days)).isoformat()
    with logged_run("prices") as res:
        with SessionLocal() as s:
            symbols = list(s.scalars(select(Company.yahoo_symbol).where(Company.is_active)))
            df = provider.fetch_prices(symbols, start=start)
            failed = df.attrs.get("failed", [])
            res["failed"] = len(failed)
            if symbols and len(failed) / len(symbols) > FAIL_TOLERANCE:
                raise RuntimeError(f"{len(failed)} dari {len(symbols)} ticker gagal")
            if df.empty:
                return res
            df["ticker"] = df["symbol"].str.removesuffix(".JK")
            df = df.dropna(subset=["close"]).copy()
            df["value_traded"] = df["close"] * df["volume"].fillna(0)
            df["is_suspect"] = flag_suspect(df)
            cols = ["ticker", "date", "open", "high", "low", "close", "adj_close",
                    "volume", "value_traded", "is_suspect"]
            out = df[cols].rename(columns={"date": "trade_date"})
            out = out.astype(object).where(out.notna(), None)
            res["rows"] = upsert(s, PriceDaily, out.to_dict("records"), ["ticker", "trade_date"])
            s.commit()
    return res
```

Job `ingest_actions.py`, `ingest_fundamentals.py`, dan `sync_companies.py` mengikuti pola yang sama: ambil daftar dari DB, panggil provider, bersihkan `NaN` menjadi `None`, `upsert`, dan dibungkus `logged_run`. `sync_companies` membaca `data/companies_seed.csv` (kolom `ticker,name,sector_code,is_financial`) pada instalasi pertama.

### 14.3 Indikator, mesin aturan, dan sinyal

`backend/worker/indicators.py`

```python
import numpy as np
import pandas as pd

LIQUID_VALUE = 1e9   # Rp1 miliar per hari (rata-rata 20 sesi)


def compute_indicators(prices: pd.DataFrame) -> pd.DataFrame:
    """prices: ticker, date, high, low, close, volume, value_traded (float).
    Mengembalikan satu baris per (ticker, date) dengan seluruh indikator."""
    df = prices.sort_values(["ticker", "date"]).reset_index(drop=True)
    g = df.groupby("ticker")

    for n, name in [(1, "ret_1d"), (21, "ret_1m"), (63, "ret_3m"),
                    (126, "ret_6m"), (189, "ret_9m"), (252, "ret_1y")]:
        df[name] = g["close"].pct_change(periods=n, fill_method=None)

    for n in (20, 50, 150, 200):
        df[f"sma{n}"] = g["close"].transform(lambda s, n=n: s.rolling(n, min_periods=n).mean())
    df["hi_52w"] = g["close"].transform(lambda s: s.rolling(252, min_periods=120).max())
    df["lo_52w"] = g["close"].transform(lambda s: s.rolling(252, min_periods=120).min())
    df["vol_avg20"] = g["volume"].transform(lambda s: s.rolling(20, min_periods=10).mean())
    df["value_avg20"] = g["value_traded"].transform(lambda s: s.rolling(20, min_periods=10).mean())

    prev_close = g["close"].shift()
    tr = pd.concat([df["high"] - df["low"],
                    (df["high"] - prev_close).abs(),
                    (df["low"] - prev_close).abs()], axis=1).max(axis=1)
    df["atr14"] = tr.groupby(df["ticker"]).transform(lambda s: s.rolling(14, min_periods=14).mean())

    # YTD: terhadap penutupan terakhir tahun sebelumnya
    df["year"] = pd.to_datetime(df["date"]).dt.year
    ye = df.groupby(["ticker", "year"])["close"].last().rename("ye_close").reset_index()
    ye["year"] += 1
    df = df.merge(ye, on=["ticker", "year"], how="left")
    df["ret_ytd"] = df["close"] / df["ye_close"] - 1

    # RS rating: peringkat persentil 1..99 di antara saham likuid pada hari yang sama
    df["rs_raw"] = (0.4 * df["ret_3m"] + 0.2 * df["ret_6m"]
                    + 0.2 * df["ret_9m"] + 0.2 * df["ret_1y"])
    liquid = df["value_avg20"] >= LIQUID_VALUE
    ranked = df[liquid].groupby("date")["rs_raw"].rank(pct=True)
    df["rs_rating"] = (ranked * 99).round().clip(lower=1).reindex(df.index)
    return df.drop(columns=["year", "ye_close", "rs_raw"])


def add_rule_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Kolom turunan yang hanya ada di memori untuk aturan watchlist."""
    g = df.groupby("ticker")
    df["sma200_20d_ago"] = g["sma200"].shift(20)
    df["hi_20d_prev"] = g["close"].transform(lambda s: s.shift(1).rolling(20, min_periods=20).max())
    df["atr14_pct"] = df["atr14"] / df["close"]
    df["atr14_pct_20d_ago"] = df.groupby("ticker")["atr14_pct"].shift(20)
    return df
```

`backend/worker/jobs/compute_indicators.py`

```python
import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import IndicatorDaily
from worker.indicators import compute_indicators
from worker.runlog import logged_run

FLOAT_COLS = ["high", "low", "close", "volume", "value_traded"]
KEEP = ["ticker", "date", "ret_1d", "ret_1m", "ret_3m", "ret_ytd", "ret_1y", "sma20", "sma50",
        "sma150", "sma200", "hi_52w", "lo_52w", "vol_avg20", "value_avg20", "atr14", "rs_rating"]


def run(calendar_days: int = 500, write_last_sessions: int = 10) -> dict:
    with logged_run("indicators") as res:
        with SessionLocal() as s:
            df = pd.read_sql(text("""
                SELECT ticker, trade_date AS date, high, low, close, volume, value_traded
                FROM prices_daily
                WHERE NOT is_suspect AND trade_date >= CURRENT_DATE - CAST(:d AS integer)
                ORDER BY ticker, trade_date"""), s.connection(), params={"d": calendar_days})
            if df.empty:
                return res
            df[FLOAT_COLS] = df[FLOAT_COLS].astype(float)
            ind = compute_indicators(df)
            last_dates = sorted(ind["date"].unique())[-write_last_sessions:]
            out = ind[ind["date"].isin(last_dates)][KEEP].rename(columns={"date": "trade_date"})
            out["rs_rating"] = out["rs_rating"].astype("Int64")
            out = out.astype(object).where(out.notna(), None)
            res["rows"] = upsert(s, IndicatorDaily, out.to_dict("records"), ["ticker", "trade_date"])
            s.commit()
    return res
```

`backend/core/rules.py`

```python
from pathlib import Path

import pandas as pd
import yaml

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"


def load_rules(name: str) -> list[dict]:
    return yaml.safe_load((RULES_DIR / f"{name}.yaml").read_text(encoding="utf-8"))


def apply_rule(df: pd.DataFrame, expr: str, **env) -> pd.DataFrame:
    """Jalankan ekspresi pandas.query. Ekspresi berasal dari YAML di repo (tepercaya),
    TIDAK PERNAH dari input pengguna. Variabel luar dirujuk dengan awalan @."""
    return df.query(expr, local_dict=env, engine="python")
```

`backend/rules/watchlists.yaml`

```yaml
- slug: leading-stocks
  name: Leading Stocks
  description: Tren naik bertingkat, SMA200 menanjak, kuat relatif, dan likuid.
  expr: >-
    close > sma50 and sma50 > sma150 and sma150 > sma200
    and sma200 > sma200_20d_ago and rs_rating >= 70 and value_avg20 >= 1e9

- slug: focus-list
  name: Focus List
  description: Pemimpin di sektor pemimpin, harga dalam 10% dari puncak 52 minggu.
  expr: in_leading_stocks and sector_id in @leading_sector_ids and close >= 0.90 * hi_52w

- slug: setup-breakout
  name: Setup - Breakout
  description: Tembus puncak 20 sesi dengan volume minimal 1,5 kali rata-rata.
  expr: close >= hi_20d_prev and volume >= 1.5 * vol_avg20 and close > sma50

- slug: setup-pullback
  name: Setup - Pullback
  description: Koreksi ke sekitar SMA20 di dalam tren naik.
  expr: sma50 > sma200 and close > sma50 and 0.98 * sma20 <= close <= 1.02 * sma20

- slug: setup-contraction
  name: Setup - Contraction
  description: Volatilitas menyempit di atas SMA50.
  expr: atr14_pct <= 0.03 and atr14_pct < 0.8 * atr14_pct_20d_ago and close > sma50
```

`backend/worker/jobs/run_rules.py`

```python
import pandas as pd
from sqlalchemy import text

from core.db import SessionLocal, upsert
from core.models import Signal, WatchlistMember
from core.rules import apply_rule, load_rules
from worker.indicators import add_rule_columns, compute_indicators
from worker.runlog import logged_run


def leading_sector_ids(df: pd.DataFrame, top: int = 3, min_members: int = 5) -> list[int]:
    liquid = df[(df["value_avg20"] >= 1e9) & df["sector_id"].notna()]
    g = liquid.groupby("sector_id")
    stats = pd.DataFrame({
        "med_ret_3m": g["ret_3m"].median(),
        "pct_above_sma50": g.apply(lambda x: (x["close"] > x["sma50"]).mean()),
        "n": g.size(),
    })
    stats = stats[stats["n"] >= min_members]   # median bermakna hanya bila anggota cukup
    stats["score"] = (0.6 * stats["med_ret_3m"].rank(pct=True)
                      + 0.4 * stats["pct_above_sma50"].rank(pct=True))
    return stats.sort_values("score", ascending=False).head(top).index.astype(int).tolist()


def _f(x):
    return None if pd.isna(x) else round(float(x), 4)


def build_signals(today: pd.DataFrame, prev: pd.DataFrame, day) -> list[dict]:
    p = prev.set_index("ticker")[["close", "sma50", "sma200"]].add_prefix("p_")
    d = today.set_index("ticker").join(p, how="left")
    liquid = d["value_avg20"] >= 1e9
    checks = {
        "new_high": d["close"] >= d["hi_52w"],
        "new_low": d["close"] <= d["lo_52w"],
        "volume_surge": (d["volume"] >= 2 * d["vol_avg20"]) & (d["value_traded"] >= 1e9),
        "big_move": (d["ret_1d"].abs() >= 0.07) & liquid,
        "breakdown_sma50": (d["p_close"] >= d["p_sma50"]) & (d["close"] < d["sma50"]),
        "breakout_sma50": (d["p_close"] < d["p_sma50"]) & (d["close"] >= d["sma50"]),
        "breakdown_sma200": (d["p_close"] >= d["p_sma200"]) & (d["close"] < d["sma200"]),
        "breakout_sma200": (d["p_close"] < d["p_sma200"]) & (d["close"] >= d["sma200"]),
    }
    rows = []
    for kind, mask in checks.items():
        for ticker, r in d[mask.fillna(False)].iterrows():
            ratio = r["volume"] / r["vol_avg20"] if r["vol_avg20"] else None
            rows.append({"trade_date": day, "ticker": ticker, "kind": kind,
                         "detail": {"close": _f(r["close"]), "ret_1d": _f(r["ret_1d"]),
                                    "vol_ratio": _f(ratio) if ratio is not None else None}})
    return rows


def run(calendar_days: int = 500) -> dict:
    with logged_run("rules") as res:
        with SessionLocal() as s:
            px = pd.read_sql(text("""
                SELECT p.ticker, p.trade_date AS date, p.high, p.low, p.close, p.volume,
                       p.value_traded, c.sector_id
                FROM prices_daily p JOIN companies c ON c.ticker = p.ticker
                WHERE NOT p.is_suspect AND c.is_active
                  AND p.trade_date >= CURRENT_DATE - CAST(:d AS integer)"""),
                s.connection(), params={"d": calendar_days})
            if px.empty:
                return res
            for c in ["high", "low", "close", "volume", "value_traded"]:
                px[c] = px[c].astype(float)
            sector = px.groupby("ticker")["sector_id"].last()
            df = add_rule_columns(compute_indicators(px.drop(columns=["sector_id"])))
            df["sector_id"] = df["ticker"].map(sector)

            days = sorted(df["date"].unique())
            day, prev_day = days[-1], days[-2] if len(days) > 1 else None
            today = df[df["date"] == day].copy()

            rules = {r["slug"]: r for r in load_rules("watchlists")}
            leading = apply_rule(today, rules["leading-stocks"]["expr"])
            today["in_leading_stocks"] = today["ticker"].isin(leading["ticker"])
            sector_ids = leading_sector_ids(today)

            members = []
            for slug, r in rules.items():
                hit = apply_rule(today, r["expr"], leading_sector_ids=sector_ids)
                hit = hit.sort_values("rs_rating", ascending=False, na_position="last")
                members += [{"slug": slug, "trade_date": day, "ticker": t, "rank": i + 1}
                            for i, t in enumerate(hit["ticker"])]
            res["rows"] += upsert(s, WatchlistMember, members, ["slug", "trade_date", "ticker"])

            if prev_day is not None:
                sigs = build_signals(today, df[df["date"] == prev_day], day)
                res["rows"] += upsert(s, Signal, sigs, ["trade_date", "ticker", "kind"])
            s.commit()
    return res
```

Catatan: tabel `watchlists` (slug, nama, deskripsi, ekspresi) diisi dari `watchlists.yaml` oleh perintah `python -m worker.cli seed-rules` agar UI dapat menampilkan kartu aturan. Sinyal dividen dibangun terpisah dari `corporate_actions` (tanggal ex dalam jendela 5 sesi).

### 14.4 Cache, pipeline, penjadwal, dan CLI

`backend/core/cache.py`

```python
import functools
import json

import redis

from core.config import get_settings

_r = redis.Redis.from_url(get_settings().redis_url, decode_responses=True)
PREFIX = "iw:"


def cached(ttl: int = 6 * 3600):
    """Cache hasil fungsi (argumen keyword saja, nilai serializable) di Redis.
    Bila Redis mati, fungsi tetap jalan tanpa cache."""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(**kwargs):
            key = f"{PREFIX}{fn.__name__}:{json.dumps(kwargs, sort_keys=True, default=str)}"
            try:
                hit = _r.get(key)
                if hit:
                    return json.loads(hit)
            except redis.RedisError:
                pass
            out = fn(**kwargs)
            try:
                _r.setex(key, ttl, json.dumps(out, default=str))
            except redis.RedisError:
                pass
            return out
        return wrapper
    return deco


def purge() -> None:
    try:
        for k in _r.scan_iter(f"{PREFIX}*"):
            _r.delete(k)
    except redis.RedisError:
        pass
```

`backend/worker/pipeline.py`

```python
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx

from core.cache import purge
from core.config import get_settings
from providers.yahoo import YahooProvider
from worker.jobs import compute_indicators, ingest_actions, ingest_prices, run_rules

log = logging.getLogger("pipeline")
WIB = ZoneInfo("Asia/Jakarta")


def market_open_today(provider) -> bool:
    """Hari bursa = bar terakhir IHSG (^JKSE) bertanggal hari ini (WIB)."""
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
        ("actions", ingest_actions.run),
        ("indicators", compute_indicators.run),
        ("rules", run_rules.run),
    ]
    for name, fn in steps:
        result = fn()
        if result["status"] != "ok":
            alert(f"Pipeline berhenti di langkah '{name}': {result['error']}")
            return
    purge()
    log.info("Pipeline selesai")
```

`backend/worker/main.py`

```python
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from core.config import get_settings
from worker.jobs import ingest_fundamentals, sync_companies
from worker.pipeline import run_daily_pipeline


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    cfg = get_settings()
    sched = BlockingScheduler(timezone=cfg.timezone)
    common = dict(max_instances=1, coalesce=True, misfire_grace_time=3600)
    sched.add_job(run_daily_pipeline,
                  CronTrigger(day_of_week="mon-fri", hour=cfg.pipeline_hour, minute=0),
                  id="daily_pipeline", **common)
    sched.add_job(sync_companies.run, CronTrigger(day_of_week="mon", hour=6),
                  id="sync_companies", **common)
    sched.add_job(ingest_fundamentals.run, CronTrigger(day_of_week="sat", hour=8),
                  id="fundamentals", **common)
    sched.start()


if __name__ == "__main__":
    main()
```

`backend/worker/cli.py`

```python
import argparse

from worker.jobs import compute_indicators, ingest_prices, run_rules, sync_companies
from worker.pipeline import run_daily_pipeline


def main() -> None:
    p = argparse.ArgumentParser(prog="worker.cli")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed", help="isi companies dari data/companies_seed.csv")
    sub.add_parser("run-once", help="jalankan pipeline harian sekarang (abaikan cek hari bursa)")
    bf = sub.add_parser("backfill", help="isi riwayat harga lalu hitung indikator dan aturan")
    bf.add_argument("--start", default="2021-01-01")
    args = p.parse_args()

    if args.cmd == "seed":
        sync_companies.run()
    elif args.cmd == "run-once":
        run_daily_pipeline(force=True)
    elif args.cmd == "backfill":
        ingest_prices.run(start=args.start)
        compute_indicators.run(calendar_days=3650, write_last_sessions=100000)
        run_rules.run()


if __name__ == "__main__":
    main()
```

Urutan pertama kali menjalankan sistem: `alembic upgrade head`, lalu `python -m worker.cli seed`, `python -m worker.cli backfill --start 2021-01-01`, dan terakhir `python -m worker.main` untuk menyalakan penjadwal. Backfill panjang sebaiknya dipecah per tahun bila sumber data membatasi permintaan.

### 14.5 API FastAPI

`backend/app/errors.py` dan `backend/app/main.py`

```python
# app/errors.py
class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message
```

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.errors import ApiError
from app.routers import feed, market_map, meta, portfolio, screener, stocks, watchlists
from core.config import get_settings

cfg = get_settings()
app = FastAPI(title="IDX Witcher API", version="0.1.0",
              docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=cfg.cors_origins,
                   allow_methods=["GET", "POST"], allow_headers=["*"])


@app.exception_handler(ApiError)
async def api_error_handler(_: Request, exc: ApiError):
    return JSONResponse(status_code=exc.status,
                        content={"error": {"code": exc.code, "message": exc.message}})


for module in (meta, market_map, stocks, screener, watchlists, feed, portfolio):
    app.include_router(module.router, prefix="/api/v1")
```

`backend/app/routers/meta.py`

```python
from fastapi import APIRouter
from sqlalchemy import text

from core.db import SessionLocal

router = APIRouter(tags=["meta"])


@router.get("/health")
def health():
    with SessionLocal() as s:
        s.execute(text("SELECT 1"))
    return {"status": "ok"}


@router.get("/meta")
def meta():
    with SessionLocal() as s:
        as_of = s.execute(text("SELECT max(trade_date) FROM indicators_daily")).scalar()
        n = s.execute(text("SELECT count(*) FROM companies WHERE is_active")).scalar()
        run = s.execute(text(
            "SELECT job, status, finished_at FROM ingest_runs ORDER BY id DESC LIMIT 1")).mappings().first()
    return {"as_of": as_of, "active_companies": n, "last_run": dict(run) if run else None}
```

`backend/app/routers/market_map.py`

```python
from fastapi import APIRouter, Query
from sqlalchemy import text

from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["market-map"])
PERIOD_COL = {"today": "ret_1d", "1m": "ret_1m", "ytd": "ret_ytd", "1y": "ret_1y"}


@cached()
def build_market_map(period: str) -> dict:
    col = PERIOD_COL[period]          # whitelist, aman untuk f-string
    sql = text(f"""
        SELECT c.ticker, c.name, s.name AS sector,
               p.close * c.shares_outstanding AS market_cap,
               i.{col} AS change_pct, i.trade_date
        FROM indicators_daily i
        JOIN prices_daily p ON p.ticker = i.ticker AND p.trade_date = i.trade_date
        JOIN companies c ON c.ticker = i.ticker
        LEFT JOIN sectors s ON s.id = c.sector_id
        WHERE i.trade_date = (SELECT max(trade_date) FROM indicators_daily)
          AND c.is_active AND c.shares_outstanding IS NOT NULL
    """)
    with SessionLocal() as s:
        rows = s.execute(sql).mappings().all()
    data = [{"ticker": r["ticker"], "name": r["name"], "sector": r["sector"],
             "market_cap": float(r["market_cap"]),
             "change_pct": None if r["change_pct"] is None else float(r["change_pct"])}
            for r in rows]
    return {"as_of": rows[0]["trade_date"] if rows else None, "period": period, "data": data}


@router.get("/market-map")
def market_map(period: str = Query("today", pattern="^(today|1m|ytd|1y)$")):
    return build_market_map(period=period)
```

`backend/rules/menus.yaml` (contoh dua menu; 12 lainnya mengikuti bentuk yang sama)

```yaml
valuation:
  columns: [ticker, name, sector, market_cap, close, pe_ttm, pb, ps, ev_ebitda, div_yield]
  higher: [div_yield]
  lower: [pe_ttm, pb, ps, ev_ebitda]
profitability:
  columns: [ticker, name, sector, market_cap, close, roe, roa, gross_margin, op_margin, net_margin]
  higher: [roe, roa, gross_margin, op_margin, net_margin]
  lower: []
```

`backend/app/routers/screener.py`

```python
import pandas as pd
from fastapi import APIRouter, Query
from sqlalchemy import text

from app.errors import ApiError
from core.cache import cached
from core.db import SessionLocal
from core.rules import load_rules

router = APIRouter(tags=["screener"])

SQL = text("""
    SELECT c.ticker, c.name, s.code AS sector, p.close, p.trade_date,
           p.close * c.shares_outstanding AS market_cap,
           to_jsonb(i) - 'ticker' - 'trade_date' AS ind,
           to_jsonb(f) - 'ticker' - 'as_of' AS fun
    FROM companies c
    JOIN prices_daily p ON p.ticker = c.ticker
         AND p.trade_date = (SELECT max(trade_date) FROM indicators_daily)
    LEFT JOIN indicators_daily i ON i.ticker = c.ticker AND i.trade_date = p.trade_date
    LEFT JOIN LATERAL (SELECT * FROM fundamentals_snapshot x WHERE x.ticker = c.ticker
                       ORDER BY as_of DESC LIMIT 1) f ON TRUE
    LEFT JOIN sectors s ON s.id = c.sector_id
    WHERE c.is_active
""")


def add_score(df: pd.DataFrame, higher: list[str], lower: list[str]) -> pd.Series:
    parts = ([df[c].rank(pct=True) for c in higher]
             + [df[c].rank(pct=True, ascending=False) for c in lower])
    if not parts:
        return pd.Series(index=df.index, dtype=float)
    table = pd.concat(parts, axis=1)
    score = table.mean(axis=1) * 100
    return score.where(table.notna().sum(axis=1) >= 3)   # minimal 3 metrik


@cached()
def build_screener(menu: str, sector: str | None, min_mcap: float, min_value: float,
                   q: str | None, limit: int) -> dict:
    menus = load_rules("menus")
    if menu not in menus:
        raise ApiError(404, "not_found", f"Menu '{menu}' tidak ada")
    spec = menus[menu]
    with SessionLocal() as s:
        raw = s.execute(SQL).mappings().all()
    records = []
    for r in raw:
        row = {k: (float(v) if hasattr(v, "is_finite") else v) for k, v in dict(r).items()
               if k not in ("ind", "fun")}
        row.update(r["ind"] or {})
        fun = dict(r["fun"] or {})
        row["na_reason"] = fun.pop("na_reason", {}) or {}
        row.update(fun)
        records.append(row)
    cols = [*spec["columns"], "score", "na_reason"]
    df = pd.DataFrame(records)
    if df.empty:
        return {"as_of": None, "menu": menu, "columns": [*spec["columns"], "score"], "data": []}
    as_of = df["trade_date"].iloc[0]
    # kolom yang belum ada (mis. fundamental belum terisi) dibuat kosong, bukan error
    needed = {*spec["columns"], *spec["higher"], *spec["lower"], "value_avg20", "market_cap"}
    for col in needed - set(df.columns):
        df[col] = None
    df["score"] = add_score(df, spec["higher"], spec["lower"])   # skor dihitung sebelum filter
    if sector:
        df = df[df["sector"] == sector]
    df = df[(df["market_cap"].astype(float).fillna(0) >= min_mcap)
            & (df["value_avg20"].astype(float).fillna(0) >= min_value)]
    if q:
        needle = q.lower()
        df = df[df["ticker"].str.lower().str.contains(needle)
                | df["name"].str.lower().str.contains(needle)]
    key = "score" if df["score"].notna().any() else "market_cap"   # menu tanpa skor
    df = df.sort_values(key, ascending=False, na_position="last")
    if limit > 0:
        df = df.head(limit)
    data = df[cols].astype(object).where(df[cols].notna(), None).to_dict("records")
    return {"as_of": as_of, "menu": menu, "columns": [*spec["columns"], "score"], "data": data}


@router.get("/screener")
def screener(menu: str = "valuation", sector: str | None = None,
             min_mcap: float = Query(0, ge=0), min_value: float = Query(0, ge=0),
             q: str | None = Query(None, max_length=50), limit: int = Query(0, ge=0, le=1000)):
    return build_screener(menu=menu, sector=sector, min_mcap=min_mcap,
                          min_value=min_value, q=q, limit=limit)
```

`backend/app/routers/feed.py`

```python
from fastapi import APIRouter, Query
from sqlalchemy import text

from core.cache import cached
from core.db import SessionLocal

router = APIRouter(tags=["feed"])


@cached(ttl=3600)
def build_feed(days: int, kind: str | None, sector: str | None) -> dict:
    sql = text("""
        SELECT sg.trade_date, sg.ticker, c.name, s.code AS sector, sg.kind, sg.detail
        FROM signals sg
        JOIN companies c ON c.ticker = sg.ticker
        LEFT JOIN sectors s ON s.id = c.sector_id
        WHERE sg.trade_date IN (SELECT DISTINCT trade_date FROM signals
                                ORDER BY trade_date DESC LIMIT :days)
          AND (CAST(:kind AS text) IS NULL OR sg.kind = CAST(:kind AS text))
          AND (CAST(:sector AS text) IS NULL OR s.code = CAST(:sector AS text))
        ORDER BY sg.trade_date DESC, sg.ticker
    """)
    with SessionLocal() as s:
        rows = s.execute(sql, {"days": days, "kind": kind, "sector": sector}).mappings().all()
    return {"days": days, "data": [dict(r) for r in rows]}


@router.get("/feed")
def feed(days: int = Query(5, ge=1, le=20), kind: str | None = None, sector: str | None = None):
    return build_feed(days=days, kind=kind, sector=sector)
```

`backend/app/routers/portfolio.py`

```python
from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import text

from core.db import SessionLocal

router = APIRouter(tags=["portfolio"])


class QuoteIn(BaseModel):
    tickers: list[str] = Field(min_length=1, max_length=100)


@router.post("/portfolio/quote")
def quote(body: QuoteIn):
    """Hanya menerima daftar ticker; jumlah lot dan harga beli tidak pernah dikirim ke server."""
    tickers = sorted({t.strip().upper() for t in body.tickers})
    sql = text("""
        SELECT DISTINCT ON (p.ticker) p.ticker, p.close, p.trade_date, s.name AS sector
        FROM prices_daily p
        JOIN companies c ON c.ticker = p.ticker
        LEFT JOIN sectors s ON s.id = c.sector_id
        WHERE p.ticker = ANY(:t)
        ORDER BY p.ticker, p.trade_date DESC
    """)
    with SessionLocal() as s:
        rows = s.execute(sql, {"t": tickers}).mappings().all()
    return {"data": [{"ticker": r["ticker"], "close": float(r["close"]),
                      "trade_date": r["trade_date"], "sector": r["sector"]} for r in rows]}
```

Router `stocks.py` (detail + `/prices`) dan `watchlists.py` memakai pola yang sama: query SQL ke tabel hasil hitung, bungkus dengan `@cached`, kembalikan dict dengan `as_of`.

### 14.6 Frontend React

Setelah `npm create vite` (bagian 14.1), tambahkan konfigurasi Tailwind (`content: ["./index.html", "./src/**/*.{ts,tsx}"]`, `darkMode: "class"`), tiga direktif Tailwind di `src/styles/index.css`, dan token warna bagian 12 sebagai CSS variables.

`frontend/vite.config.ts`

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { "/api": "http://localhost:8000" } },
});
```

`frontend/src/api/client.ts`, `types.ts`, `hooks.ts`

```ts
// client.ts
const BASE = import.meta.env.VITE_API_BASE ?? "";

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}/api/v1${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ApiError(res.status, body?.error?.code ?? "unknown", body?.error?.message ?? res.statusText);
  }
  return res.json() as Promise<T>;
}
```

```ts
// types.ts
export type Period = "today" | "1m" | "ytd" | "1y";

export interface MarketMapRow {
  ticker: string;
  name: string;
  sector: string | null;
  market_cap: number;
  change_pct: number | null;
}

export interface MarketMapResponse {
  as_of: string | null;
  period: Period;
  data: MarketMapRow[];
}
```

```ts
// hooks.ts
import { useQuery } from "@tanstack/react-query";
import { api } from "./client";
import type { MarketMapResponse, Period } from "./types";

export const useMarketMap = (period: Period) =>
  useQuery({
    queryKey: ["market-map", period],
    queryFn: () => api<MarketMapResponse>(`/market-map?period=${period}`),
    staleTime: 5 * 60_000,
  });
```

`frontend/src/lib/format.ts`

```ts
const nf = new Intl.NumberFormat("id-ID", { maximumFractionDigits: 2 });

export const fmtNum = (v: number | null | undefined) => (v == null ? "–" : nf.format(v));

export const fmtPct = (v: number | null | undefined, digits = 2) =>
  v == null
    ? "–"
    : `${v > 0 ? "+" : ""}${(v * 100).toLocaleString("id-ID", {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits,
      })}%`;

/** Rupiah dengan singkatan Indonesia: T (triliun), M (miliar), Jt (juta). */
export function fmtRp(v: number | null | undefined): string {
  if (v == null) return "–";
  const a = Math.abs(v);
  if (a >= 1e12) return `Rp${nf.format(v / 1e12)} T`;
  if (a >= 1e9) return `Rp${nf.format(v / 1e9)} M`;
  if (a >= 1e6) return `Rp${nf.format(v / 1e6)} Jt`;
  return `Rp${nf.format(v)}`;
}
```

`frontend/src/components/charts/MarketMap.tsx`

```tsx
import { useEffect, useMemo, useRef } from "react";
import * as echarts from "echarts/core";
import { TreemapChart } from "echarts/charts";
import { TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import type { MarketMapRow } from "../../api/types";
import { fmtPct, fmtRp } from "../../lib/format";

echarts.use([TreemapChart, TooltipComponent, CanvasRenderer]);

const SMALL_MCAP = 5e11; // Rp500 miliar
const BOTTOM_SHARE = 0.05; // 5% kumulatif terbawah per sektor

function colorFor(change: number | null, limit: number): string {
  if (change == null) return "#4b5563";
  const t = Math.max(-1, Math.min(1, change / limit));
  const base = [75, 85, 99];
  const target = t >= 0 ? [34, 197, 94] : [248, 113, 113];
  const k = Math.abs(t);
  return `rgb(${base.map((b, i) => Math.round(b + (target[i] - b) * k)).join(",")})`;
}

function buildTree(rows: MarketMapRow[], limit: number) {
  const bySector = new Map<string, MarketMapRow[]>();
  for (const r of rows) {
    const key = r.sector ?? "Lainnya";
    const list = bySector.get(key) ?? [];
    list.push(r);
    bySector.set(key, list);
  }
  return [...bySector.entries()].map(([sector, list]) => {
    const asc = [...list].sort((a, b) => a.market_cap - b.market_cap);
    const total = asc.reduce((s, r) => s + r.market_cap, 0);
    let cum = 0;
    const big: MarketMapRow[] = [];
    const small: MarketMapRow[] = [];
    for (const r of asc) {
      cum += r.market_cap;
      (cum / total <= BOTTOM_SHARE || r.market_cap < SMALL_MCAP ? small : big).push(r);
    }
    const leaf = (r: MarketMapRow) => ({
      name: r.ticker,
      ticker: r.ticker,
      leaf: true,
      value: r.market_cap,
      pct: fmtPct(r.change_pct, 1),
      tip: `${r.name}<br/>${fmtPct(r.change_pct)} · ${fmtRp(r.market_cap)}`,
      itemStyle: { color: colorFor(r.change_pct, limit) },
    });
    const children = big.map(leaf);
    if (small.length) {
      const mc = small.reduce((s, r) => s + r.market_cap, 0);
      const avg = small.reduce((s, r) => s + (r.change_pct ?? 0) * r.market_cap, 0) / mc;
      children.push({
        name: `Lainnya (${small.length})`, ticker: "", leaf: false, value: mc,
        pct: fmtPct(avg, 1), tip: `${small.length} saham kecil<br/>${fmtPct(avg)}`,
        itemStyle: { color: colorFor(avg, limit) },
      });
    }
    return { name: sector, children };
  });
}

export function MarketMap({ rows, onSelect }: { rows: MarketMapRow[]; onSelect: (ticker: string) => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const limit = useMemo(() => {
    const abs = rows.map((r) => Math.abs(r.change_pct ?? 0)).sort((a, b) => a - b);
    return Math.max(0.05, abs[Math.floor(abs.length * 0.9)] ?? 0.05); // minimal ±5%
  }, [rows]);
  const data = useMemo(() => buildTree(rows, limit), [rows, limit]);

  useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current, undefined, { renderer: "canvas" });
    chart.setOption({
      tooltip: { formatter: (p: any) => `${p.name}<br/>${p.data?.tip ?? ""}` },
      series: [{
        type: "treemap", roam: false, nodeClick: false, breadcrumb: { show: false },
        left: 0, right: 0, top: 0, bottom: 0,
        label: { show: true, formatter: (p: any) => (p.data?.pct ? `${p.name}\n${p.data.pct}` : p.name) },
        upperLabel: { show: true, height: 18, color: "#e6eaf0" },
        itemStyle: { borderColor: "#0d1117", borderWidth: 1, gapWidth: 1 },
        data,
      }],
    });
    chart.on("click", (p: any) => p.data?.leaf && onSelect(p.data.ticker));
    const ro = new ResizeObserver(() => chart.resize());
    ro.observe(ref.current);
    return () => { ro.disconnect(); chart.dispose(); };
  }, [data, onSelect]);

  return (
    <div ref={ref} className="h-[70vh] w-full" role="img"
         aria-label="Peta pasar saham IDX menurut kapitalisasi pasar dan perubahan harga" />
  );
}
```

`frontend/src/pages/Explore.tsx`

```tsx
import { useState } from "react";
import { useMarketMap } from "../api/hooks";
import type { Period } from "../api/types";
import { MarketMap } from "../components/charts/MarketMap";

const PERIODS: { id: Period; label: string }[] = [
  { id: "today", label: "Today" }, { id: "1m", label: "1 month" },
  { id: "ytd", label: "YTD" }, { id: "1y", label: "1 year" },
];

export default function Explore() {
  const [period, setPeriod] = useState<Period>("today");
  const [selected, setSelected] = useState<string | null>(null);
  const { data, isLoading, error, refetch } = useMarketMap(period);

  return (
    <section className="p-4">
      <div className="mb-3 flex items-center gap-2">
        {PERIODS.map((p) => (
          <button key={p.id} onClick={() => setPeriod(p.id)}
            className={`rounded px-3 py-1 text-sm ${period === p.id ? "bg-[--accent] text-white" : "border"}`}>
            {p.label}
          </button>
        ))}
        {data?.as_of && <span className="ml-auto text-xs text-[--muted]">Harga per {data.as_of}</span>}
      </div>
      {isLoading && <div className="h-[70vh] animate-pulse rounded bg-[--surface]" />}
      {error && <button onClick={() => refetch()} className="underline">Gagal memuat. Coba lagi</button>}
      {data && <MarketMap rows={data.data} onSelect={setSelected} />}
      {selected && <p className="mt-2 text-sm">Dipilih: {selected}</p>}
    </section>
  );
}
```

`frontend/src/store/portfolio.ts`

```ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface Holding {
  id: string; ticker: string; lots: number; avgPrice: number; fee?: number; boughtAt?: string;
}
interface State {
  holdings: Holding[];
  add: (h: Omit<Holding, "id">) => void;
  remove: (id: string) => void;
  clear: () => void;
}

export const usePortfolio = create<State>()(
  persist(
    (set) => ({
      holdings: [],
      add: (h) => set((s) => ({ holdings: [...s.holdings, { ...h, id: crypto.randomUUID() }] })),
      remove: (id) => set((s) => ({ holdings: s.holdings.filter((x) => x.id !== id) })),
      clear: () => set({ holdings: [] }),
    }),
    { name: "idxw-portfolio-v1" },
  ),
);

/** 1 lot = 100 lembar. */
export function valueHolding(h: Holding, close: number) {
  const shares = h.lots * 100;
  const cost = shares * h.avgPrice + (h.fee ?? 0);
  const value = shares * close;
  return { shares, cost, value, pnl: value - cost, pnlPct: cost ? (value - cost) / cost : 0 };
}
```

`frontend/src/components/table/NaCell.tsx`

```tsx
const HINT: Record<string, string> = {
  bank: "Rasio ini tidak berlaku untuk bank, asuransi, dan perusahaan pembiayaan.",
  "no data": "Tidak ada laporan keuangan di sumber data.",
  loss: "Laba TTM negatif, sehingga rasio tidak bermakna.",
  "n/a": "Tidak dilaporkan atau dibuang oleh pemeriksaan kualitas data.",
};

export function NaCell({ reason }: { reason?: string }) {
  const key = reason && HINT[reason] ? reason : "n/a";
  return <span className="text-[--muted]" title={HINT[key]}>{key}</span>;
}
```

Pola `DataTable` (TanStack Table) untuk screener: definisikan kolom dari `response.columns`, render sel `null` dengan `<NaCell reason={row.na_reason?.[col]} />`, aktifkan `getSortedRowModel()`, dan tambahkan `@tanstack/react-virtual` bila baris melewati 200. Tes unit pertama yang disarankan: `fmtRp`, `fmtPct`, dan `valueHolding` dengan kasus hitung tangan.
