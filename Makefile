.PHONY: build run dev test clean

build:
	docker build -t triage-api .

run:
	docker run --rm -p 8000:8000 --env-file .env triage-api

dev:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
