@echo off
REM Start IDX Witcher backend + Cloudflare tunnel

cd /d "C:\Users\asus_\OneDrive\Documents\idx-witcher\apps\api"
set PYTHONPATH=src

REM Kill existing processes (if any)
taskkill /F /IM python.exe /FI "WINDOWTITLE eq uvicorn*" 2>nul
taskkill /F /IM cloudflared.exe 2>nul

REM Create persistent DB dir
cd /d "C:\Users\asus_\OneDrive\Documents\idx-witcher"

REM Start Uvicorn in a new window
start "idx-witcher-api" cmd /c "cd /d C:\Users\asus_\OneDrive\Documents\idx-witcher\apps\api && set PYTHONPATH=src && python -m uvicorn idxwitcher_api.main:app --host 0.0.0.0 --port 8000 --workers 1"

REM Wait for API to be ready
:wait_api
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    timeout /t 2 >nul
    goto wait_api
)

REM Start Cloudflare tunnel in a new window
timeout /t 2 >nul
start "idx-witcher-tunnel" cmd /k "C:\Users\asus_\AppData\Local\bin\cloudflared.exe tunnel --url http://localhost:8000"

echo API running at http://localhost:8000
echo Cloudflare tunnel starting. Tunggu URL muncul di jendela tunnel.
pause
