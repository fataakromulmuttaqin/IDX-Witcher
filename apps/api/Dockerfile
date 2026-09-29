FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency metadata
COPY pyproject.toml ./
COPY src ./src

# Install dependencies
RUN uv pip install --system -e .

# Copy full source
COPY . ./

EXPOSE 8000

CMD ["uvicorn", "Alpha Cygni_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
