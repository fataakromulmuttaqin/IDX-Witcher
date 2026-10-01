.PHONY: up seed backfill test lint typecheck

up:
	docker compose up -d --build

seed:
	docker compose run --rm api python -m worker.cli seed

backfill:
	docker compose run --rm api python -m worker.cli backfill --start 2021-01-01

test:
	cd backend && pytest -q

lint:
	cd backend && ruff check .

cd backend && mypy .
