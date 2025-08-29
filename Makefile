.PHONY: fmt lint test up down api

fmt:
	ruff --fix . && black . && isort .

lint:
	ruff . && mypy .

test:
	pytest -q

up:
	docker compose up -d

down:
	docker compose down -v

api:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
