# Client Portal

This is a multi-tenant client portal.

## Getting Started (Dev)

1. Install deps: `pip install -r requirements.txt` and `npm install`
2. Copy `.env.example` to `.env` (defaults to SQLite at `instance/app.db`).
3. Build CSS: `npm run build-css` (or `make build-css`)
4. Initialize DB schema: `flask --app app.py db upgrade`
5. Seed demo (optional): `python manage.py seed-demo`
6. Start dev server: `make dev`

## Quick Commands

```
# from project root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
cp .env.example .env
flask --app app.py db upgrade
npm run build-css
make dev
# optional demo data
python manage.py seed-demo
```

## Database Reset

If you need a clean database locally, use:

```
make reset-db
```

This target backs up `instance/app.db` to `instance/app.db.bak` (if present), deletes the DB, runs migrations, and seeds demo data. It uses an absolute `DATABASE_URL` to avoid path issues on some systems.
```

## Production Notes

- Set `DATABASE_URL` to your Postgres URL.
- Configure rate limiting storage via `RATELIMIT_STORAGE_URI` (e.g., `redis://host:6379/0`).
- Set secure cookies: `SESSION_COOKIE_SECURE=1`, `REMEMBER_COOKIE_SECURE=1`.
- Configure mail to enable notifications (`MAIL_*` vars in `.env.example`).
- Serve with `gunicorn`: `make run`.
