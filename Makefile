.PHONY: dev lint fmt test build-css run migrate db-upgrade db-reset reset-db

dev:
	flask --app app.py run

lint:
	ruff check .

fmt:
	ruff format .

test:
	pytest

build-css:
	./node_modules/.bin/tailwindcss -i app/static/css/input.css -o app/static/css/app.css

run:
	gunicorn -w 4 'app:app'

migrate:
	flask db migrate

db-upgrade:
	flask --app app.py db upgrade

db-reset:
	rm -f instance/app.db && flask --app app.py db upgrade && python manage.py seed-demo

reset-db:
	@DB="sqlite:///$$(pwd)/instance/app.db"; \
	if [ -f instance/app.db ]; then cp instance/app.db instance/app.db.bak; fi; \
	rm -f instance/app.db; \
	DATABASE_URL="$$DB" flask --app app.py db upgrade; \
	DATABASE_URL="$$DB" python manage.py seed-demo
