# Local Deployment Guide (PC + Cloudflare Tunnel)

## Cara Menjalankan IDX Witcher di Local

### 1. Start Server
Jalankan satu kali:
```bat
scripts\start_local_server.bat
```

Ini akan:
- Kill process lama
- Start FastAPI di port 8000
- Tunggu API ready
- Start Cloudflare tunnel

Setelah tunnel berjalan, salin URL `https://xxx.trycloudflare.com`.

### 2. Update Vercel
Jalankan:
```bat
scripts\update_vercel_env.bat
```

Masukkan URL tunnel, lalu script akan:
- Set `NEXT_PUBLIC_API_URL` di Vercel
- Deploy ulang frontend

### 3. Stop Server
```bat
scripts\stop_local_server.bat
```

## Penting

- Cloudflare tunnel URL berubah tiap restart.
- PC harus tetap nyala supaya backend online.
- Kalau mau URL permanen, pakai Cloudflare account + named tunnel.
