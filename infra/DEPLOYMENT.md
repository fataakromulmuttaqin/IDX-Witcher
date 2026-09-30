# IDX Witcher - Deployment Architecture (Hemat)

## Arsitektur Target (Free Tier)

```
┌─────────────────────────────────────────────┐
│                  Vercel                      │
│            Next.js Frontend                  │
│       Static Export + Edge Network           │
└─────────────┬───────────────────────────────┘
              │
              │ NEXT_PUBLIC_API_URL
              │
┌─────────────▼───────────────────────────────┐
│           Render / Railway                 │
│         FastAPI Backend                    │
│         Python 3.11 Docker                   │
└─────────────┬───────────────────────────────┘
              │
              │ DATABASE_URL
              │
┌─────────────▼───────────────────────────────┐
│         Neon PostgreSQL (Free)               │
│         atau SQLite untuk dev/test          │
└─────────────────────────────────────────────┘
```

## Komponen

| Layer | Layanan | Biaya |
|---|---|---|
| Frontend | Vercel Hobby | Gratis |
| Backend API | Render Web Service Free | Gratis |
| Database | Neon PostgreSQL Free Tier | Gratis |
| Cache | Tidak dipakai dulu | - |
| Cron | APScheduler internal FastAPI | - |
| Storage | Local FS / sementara | - |

## Kenapa Render untuk Backend?

- Gratis tier tersedia selamanya
- Native FastAPI + Docker support
- GitHub integration otomatis
- HTTPS otomatis
- Cocok untuk API kecil/MVP

## Kenapa Neon PostgreSQL?

- Free tier 500 MB storage
- Serverless, scale-to-zero
- Connection string mudah
- Bisa hidup terus walau backend sleep

## Kenapa Vercel untuk Frontend?

- Sudah deploy dan berjalan
- Static export tanpa server runtime
- Edge CDN global gratis

## Langkah Deploy Backend ke Render

1. Buka https://dashboard.render.com/
2. Create New Web Service
3. Connect GitHub repo `fataakromulmuttaqin/idx-witcher`
4. Pilih root directory: `apps/api`
5. Build command: kosongkan (sudah pakai Dockerfile)
6. Start command: kosongkan (sudah pakai Dockerfile CMD)
7. Environment Variables:
   - `DATABASE_URL`: connection string dari Neon
   - `REDIS_URL`: kosongkan
   - `CORS_ORIGINS`: URL Vercel frontend

## Langkah Deploy Database ke Neon

1. Buka https://neon.tech
2. Sign up / Sign in
3. Create new project
4. Copy connection string
5. Paste ke Environment Variables Render sebagai `DATABASE_URL`

## Langkah Deploy Frontend ke Vercel

1. Buka https://vercel.com/new
2. Import repo `idx-witcher`
3. Pilih framework preset: Next.js
4. Root directory: `apps/web`
5. Environment variable:
   - `NEXT_PUBLIC_API_URL`: URL backend Render
6. Deploy

## File Konfigurasi Deployment

- `apps/api/Dockerfile` — Docker image backend
- `infra/railway.json` — Railway config (opsional)
- `infra/Procfile` — Heroku-style deployment (opsional)
- `apps/web/next.config.ts` — Static export config

## Notes

- Render free tier akan sleep setelah idle. Request pertama setelah idle memerlukan waktu startup beberapa detik.
- Neon PostgreSQL free tier memiliki batas 500 MB.
- Jangan commit file `.env` ke GitHub.
- Untuk production scale, pertimbangkan upgrade ke paid tier.
