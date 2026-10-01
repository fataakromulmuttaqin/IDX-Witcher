#!/bin/bash
# IDX Witcher local server launcher (Git Bash / MSYS)

set -e

BASE_DIR="/c/Users/asus_/OneDrive/Documents/idx-witcher"
API_DIR="$BASE_DIR/apps/api"
CLOUDFLARE_BIN="$LOCALAPPDATA/bin/cloudflared.exe"

# Kill existing
taskkill //IM python.exe //F 2>/dev/null || true
taskkill //IM cloudflared.exe //F 2>/dev/null || true

# Start API
cd "$API_DIR"
export PYTHONPATH=src
python -m uvicorn idxwitcher_api.main:app --host 0.0.0.0 --port 8000 --workers 1 &
API_PID=$!

# Wait for API
for i in {1..30}; do
    curl -s http://localhost:8000/health >/dev/null 2>&1 && break
    sleep 2
done

# Start tunnel
"$CLOUDFLARE_BIN" tunnel --url http://localhost:8000 &
TUNNEL_PID=$!

# Wait for tunnel URL
for i in {1..30}; do
    sleep 3
    URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' ~/.cloudflared/*.log 2>/dev/null | head -n 1 || true)
    if [ -n "$URL" ]; then
        echo "Tunnel URL: $URL"
        break
    fi
done

echo "API PID: $API_PID"
echo "Tunnel PID: $TUNNEL_PID"
wait
