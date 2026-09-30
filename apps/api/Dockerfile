FROM python:3.11-slim

WORKDIR /app

# Install system deps for yfinance/pandas + curl-cffi
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip deps (fallback if uv unavailable)
RUN pip install --no-cache-dir uv || echo "uv not required"

COPY pyproject.toml ./
COPY src ./src

# Prefer uv, fallback to pip install editable
RUN (uv pip install --system -e .) || (pip install --no-cache-dir -e .)

COPY . ./

EXPOSE 8000

CMD ["uvicorn", "idxwitcher_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
