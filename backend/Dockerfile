FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=Asia/Jakarta
WORKDIR /app
COPY pyproject.toml ./
COPY core ./core
COPY providers ./providers
COPY worker ./worker
COPY app ./app
COPY rules ./rules
COPY data ./data
COPY alembic ./alembic
COPY alembic.ini ./
RUN pip install --no-cache-dir -e .
