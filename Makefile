.PHONY: dev lint fmt test build-css run migrate

dev:
	flask run

lint:
	ruff check .

fmt:
	ruff format .

test:
	pytest

build-css:
	tailwindcss -i app/static/css/input.css -o app/static/css/app.css

run:
	gunicorn -w 4 'app:app'

migrate:
	flask db migrate
