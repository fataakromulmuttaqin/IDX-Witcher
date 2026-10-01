FROM python:3.11-slim

WORKDIR /app

# Install system deps for yfinance/pandas + curl-cffi
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first for layer caching
COPY pyproject.toml ./
COPY src ./src

# Install project with all dependencies
RUN pip install --no-cache-dir -e .

# Copy the rest of the application
COPY . ./

EXPOSE 8000

CMD ["uvicorn", "idxwitcher_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
