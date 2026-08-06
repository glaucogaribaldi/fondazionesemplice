.PHONY: help env validate test mock-up gpu-up down logs

help:
	@printf '%s\n' 'make env       Create .env from template' 'make validate  Validate configuration' 'make test      Run unit tests' 'make mock-up   Start CPU/mock stack' 'make gpu-up    Start L4 production stack' 'make down      Stop stack'

env:
	@test -f .env || cp .env.example .env

validate:
	python3 scripts/validate_config.py

test:
	python3 -m unittest discover -s tests -v

mock-up: env
	docker compose --profile mock --profile observability up -d --build

gpu-up: env
	docker compose --profile gpu --profile observability up -d --build

down:
	docker compose --profile mock --profile gpu --profile observability down

logs:
	docker compose logs -f --tail=200
