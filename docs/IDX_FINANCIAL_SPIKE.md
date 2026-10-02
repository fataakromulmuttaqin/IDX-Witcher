# Spike: Analisis Laporan Keuangan IDX.co.id

> Tanggal: 2 Okt 2026 — Status: SPIKE (belum di-merge)
> Sumber verifikasi: extract idx.co.id/laporan-keuangan-dan-tahunan + archive/original + curl WAF test

## 1. Temuan

Halaman `idx.co.id/id/perusahaan-tercatat/laporan-keuangan-dan-tahunan` **bukan HTML statis**.

Extract menunjukkan tiap emiten (AADI, AALI, ABBA ...) punya bundle:
```
FinancialStatement-2026-I-XXXX.pdf
FinancialStatement-2026-I-XXXX.xlsx
instance.zip            ← XBRL instance (terstruktur)
inlineXBRL.zip          ← XBRL inline
Surat Pernyataan Direksi
```

Halaman itu sendiri hanya shell — data di-load via XHR:
```
POST /primary/FinancialStatementOfIssuer/GetFinancialStatement?year=2026&period=I&kodeEmiten=BBCA
POST /primary/RegisteredIssuer/GetIssuer?year=2026
```

### WAF
`curl -A Mozilla -H referer` polos → `403 Forbidden` + `cf_chl_opt` (Cloudflare Turnstile).
Browser automated juga timeout 420s di challenge page.

`archive/original/docs/DATA_SOURCES.md` sudah mencatat:
> `idx.co.id sering memblokir request otomatis karena WAF.`

**Kesimpulan:** scraping HTML mentah tidak viable. Ada 3 jalur:

| Jalur | Cara | Keandalan | Kompleksitas |
|-------|------|-----------|--------------|
| A. Manual XLSX | User upload `FinancialStatement-*.xlsx` ke `backend/data/` | Tinggi | Rendah |
| B. XHR API | Hit `GetFinancialStatement` dengan header+cookie bypass | Sedang (WAF berubah) | Sedang |
| C. XBRL ZIP | Download + parse `instance.zip` → mapping IFRS | Tinggi (source of truth) | Tinggi |

Rekomendasi: **A untuk MVP (Fase 2 awal), C untuk automation.**

## 2. Format Data (dari extract)

- `FinancialStatement-YYYY-P-XXXX.xlsx` — Excel dengan sheet IS/BS/CF
- `instance.zip` — berisi `*.xbrl` / `*.xml` dengan tag IFRS: `ifrs-full:Revenue`, `ProfitLoss`, `Assets`, `Equity`, `CashFlows` dll.
- `inlineXBRL.zip` — HTML+XBRL inline

Mapping ke tabel `financial_statements` yang sudah ada di PRD (item = `TotalRevenue`, `NetIncome` dll) — 1x mapping.

## 3. Arsitektur yang Diusulkan

```
YahooProvider (harga harian, TTM fallback)
     ↓
IDXProvider (LK resmi, prioritas)  →  financial_statements (source='idx')
     ↓
compute_snapshot()  — pakai IDX jika ada, fallback Yahoo
     ↓
fundamentals_snapshot (market_cap, pe_ttm, roe, na_reason)
```

Slot PRD `providers/idx_files.py` → diisi `providers/idx.py`.

### Pipeline
```
providers/idx.py:
  - fetch_report_list(ticker=None, year, period) → list {ticker, year, period, files: {xlsx_url, instance_url}}
  - download_xlsx(url) → DataFrame
  - parse_instance_zip(zip_bytes) → dict {item: value}  (XBRL → long format)
  - to_long_format(ticker, period_end, statement, item, value) → rows for financial_statements

worker/jobs/import_idx_reports.py:
  - loop companies (is_active)
  - cek apakah period_end terbaru sudah ada di financial_statements
  - download hanya yang baru → upsert
  - panggil compute_snapshot ulang untuk ticker tersebut

worker/pipeline.py:
  - ingest_fundamentals pakai Yahoo mingguan
  - import_idx_reports bulanan/ketika ada laporan baru (prioritas overwrite)
```

### Tabel
Tidak butuh tabel baru. Pakai existing:
- `financial_statements` (tambah `source='idx'` atau `'yfinance'`)
- `fundamentals_snapshot` (hasil hitung `worker/fundamentals.py` sudah ada — tinggal prioritas IDX)

Opsional cache raw:
- `backend/data/idx_reports/{ticker}/{period}.zip` — simpan ZIP agar re-run tidak hit IDX lagi (sesuai PRD: simpan hasil mentah).

## 4. Frontend — Fitur Analisis LK (baru)

Rute baru (Fase 2):
```
/stock/:ticker/laporan   → tabel LK 5 kuartal (Revenue, Gross Profit, Net Income, Assets, Equity, Cash)
/stock/:ticker/analisis  → tren margin/ROE/DER + tombol download XBRL asli
/screener  → tambah filter berbasis IDX (sudah ada: rev_growth_yoy dari LK)
```

Komponen:
- `ReportTable` — pivot financial_statements per period_end
- `TrendChart` — lightweight-charts line untuk 3 metrik pilihan
- API: `GET /stocks/{ticker}/reports?limit=5`, `GET /stocks/{ticker}/reports/{period}.xlsx`

## 5. Risiko & Mitigasi

| Risiko | Mitigasi |
|--------|----------|
| WAF Cloudflare blokir | Jangan hit tiap hari; cache ZIP; fallback manual upload; pakai `playwright-stealth` jika butuh bypass (jalan di worker, bukan API) |
| Nama kolom XLSX berubah | Konstanta `IDX_COLS` + test `test_idx_mapping` (fail loud) |
| Mapping IFRS → item IDX-Witcher | Buat `xbrl_map.yaml` (ifrs-full:Revenue → TotalRevenue) — review manual |
| Laporan USD vs IDR | Pakai `financialCurrency` dari XBRL + kurs IDR=X (sudah ada di compute_snapshot) |
| Ticker 800+ ZIP besar | Download inkremental: hanya ticker yang period_end belum ada; batch 20 + sleep 2s; retry |

## 6. Estimasi

- **Spike A (manual XLSX upload + parser):** 1-2 hari — `read_excel → to_long_format → upsert`
- **Spike B (XHR listing):** 0.5 hari — butuh bypass header (archive/original `idx_client.py` sudah ada template)
- **Spike C (XBRL ZIP parse):** 2-3 hari — `zipfile + xml.etree + xbrl_map.yaml`
- **UI laporan:** 1-2 hari setelah data masuk

## 7. Langkah Selanjutnya (jika di-approve)

1. Scaffold `backend/providers/idx.py` (sudah dibuat stub)
2. Implement `parse_xlsx` untuk `FinancialStatement-*.xlsx` (paling cepat deliver value)
3. Tambah `worker/jobs/import_idx_reports.py` + `worker/cli.py import-idx`
4. Test dengan 3 emiten (BBCA, TLKM, ASII) — verify vs Yahoo
5. Baru tambah frontend `/stock/:ticker/laporan`

## 8. Alternatif Tanpa Scraping (jika WAF terlalu ketat)

- **IDN Financials / idx-bei API** (repo `nichsedge/idx-bei` — disebut di archive README) — wrapper tidak resmi yang sudah handle WAF.
- **Beli data dari TICMI / RTI Business** — untuk komersial, ganti DataProvider tanpa ubah pipeline (sesuai PRD §6).

## Referensi
- `archive/original/apps/api/src/idxwitcher_api/services/idx_client.py` — client TradingSummary (bukan LK, tapi pola header/retry sama)
- `archive/original/docs/DATA_SOURCES.md`
- `docs/PRD.md` §6 (Sumber Data), §9 (Pipeline), §14.7 (fundamentals.py)
