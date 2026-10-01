@echo off
REM Capture Cloudflare tunnel URL and update Vercel env

set /p TUNNEL_URL="Masukkan URL Cloudflare tunnel (contoh: https://xxxx.trycloudflare.com): "

if "%TUNNEL_URL%"=="" (
    echo URL tidak boleh kosong.
    exit /b 1
)

cd /d "C:\Users\asus_\OneDrive\Documents\idx-witcher\apps\web"

echo Mengupdate NEXT_PUBLIC_API_URL=%TUNNEL_URL% di Vercel...
npx vercel env rm NEXT_PUBLIC_API_URL production -y 2>nul
npx vercel env add NEXT_PUBLIC_API_URL production

npx vercel --prod --yes

echo Done.
pause
