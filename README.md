# Client Portal

This is a multi-tenant client portal.

## How to run (dev)

1. Install deps: `pip install -r requirements.txt` and `npm install`
2. Copy `.env.example` to `.env` (defaults to SQLite at `instance/app.db`).
3. Initialize DB schema: `flask --app app.py db upgrade`
4. Seed demo (optional): `python manage.py seed_demo`
5. Run the dev server: `make dev`
