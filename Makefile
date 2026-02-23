.PHONY: build run dev test lint clean

build:
	docker compose build

run:
	docker compose up

dev:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -v

lint:
	ruff check app/ tests/

clean:
	docker compose down --rmi local
	find . -type d -name __pycache__ -exec rm -rf {} +
