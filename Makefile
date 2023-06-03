install:
		poetry install

dev:
		poetry run flask --app page_analyzer:app run --debug

PORT ?= 8000
start:
		poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

db-create:
	createdb page_analyzer || echo 'skip'

db-reset:
	dropdb page_analyzer || true
	createdb page_analyzer
	psql page_analyzer < database.sql

connect:
	psql -d page_analyzer

lint:
		poetry run flake8 page_analyzer

test:
		poetry run pytest

test-cov:
		poetry run pytest --cov=gendiff

selfcheck:
		poetry check

#check: selfcheck test lint

.PHONY: install test lint selfcheck check build
