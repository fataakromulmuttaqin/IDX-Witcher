@echo off
cd /d "C:\Users\asus_\OneDrive\Documents\idx-witcher\apps\api"
set PYTHONPATH=src
python -m uvicorn idxwitcher_api.main:app --host 0.0.0.0 --port 8000 --workers 1
