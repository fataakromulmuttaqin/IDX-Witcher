# IDX Witcher - Deploy Backend ke Render (Hemat)

## Cara Deploy via Browser (Recommended)

### 1. Login ke Render
- Buka https://dashboard.render.com
- Login dengan GitHub

### 2. Deploy Database PostgreSQL
1. Klik **New +** → **PostgreSQL**
2. Isi:
   - Name: `idx-witcher-db`
   - Database: `idxwitcher`
   - User: `idxwitcher`
3. Pilih plan **Free**
4. Klik **Create Database**
5. Copy **Internal Database URL** ke notepad

### 3. Deploy Web Service
1. Klik **New +** → **Web Service**
2. Pilih repo GitHub: `fataakromulmuttaqin/idx-witcher`
3. Konfigurasi:
   - Name: `idx-witcher-api`
   - Environment: `Docker`
   - Root Directory: `apps/api`
   - Branch: `main`
4. Environment Variables:
   - `DATABASE_URL` = paste dari notepad
   - `CORS_ORIGINS` = `https://web-flax-eight-69.vercel.app,http://localhost:3000,http://127.0.0.1:3000`
   - `FINNHUB_API_KEY` = `daua10pr01qkvn4ovhi0daua10pr01qkvn4ovhig`
5. Klik **Create Web Service**

### 4. Init Database
Setelah service running, buka Shell di Render Dashboard:
```bash
cd /app
python init_db.py
python -c "from idxwitcher_api.services.tv_sync import sync_companies_from_tradingview; from idxwitcher_api.db.session import SessionLocal; sync_companies_from_tradingview(SessionLocal())"
```

### 5. Update Frontend API URL
1. Buka Vercel Dashboard → project `idx-witcher`
2. Tambahkan environment variable:
   - `NEXT_PUBLIC_API_URL` = URL backend Render (contoh: `https://idx-witcher-api.onrender.com`)
3. Redeploy frontend

## URL Penting
- Frontend: https://web-flax-eight-69.vercel.app
- Backend: https://idx-witcher-api.onrender.com (setelah deploy)

## Troubleshooting
- Render free tier sleep setelah idle. Request pertama bisa lambat 10-30 detik.
- Kalau port error, cek `Dockerfile` expose port 8000.
- Kalau DB error, pastikan `DATABASE_URL` valid dan tabel sudah dibuat.
