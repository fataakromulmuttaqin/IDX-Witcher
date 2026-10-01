@echo off
REM Stop IDX Witcher API + Cloudflare tunnel

taskkill /FI "WINDOWTITLE eq idx-witcher-api*" /F 2>nul
taskkill /FI "WINDOWTITLE eq idx-witcher-tunnel*" /F 2>nul
taskkill /IM python.exe /F 2>nul
taskkill /IM cloudflared.exe /F 2>nul

echo IDX Witcher stopped.
pause
