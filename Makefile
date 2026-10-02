.PHONY: up seed seed-rules backfill run-once test lint typecheck

up:
	docker compose up -d --build

seed:
	docker compose run --rm api python -m worker.cli seed

seed-rules:
	docker compose run --rm api python -m worker.cli seed-rules

backfill:
	docker compose run --rm api python -m worker.cli backfill --start 2021-01-01

run-once:
	docker compose run --rm worker python -m worker.cli run-once

test:
	cd backend && pytest -q

lint:
	cd backend && ruff check .

typecheck:
	cd backend && mypy .
