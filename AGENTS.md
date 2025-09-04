# Repository Guidelines

## Project Structure & Module Organization
- app/: Flask app with blueprints (`auth/`, `org/`, `threads/`, `tasks/`, `files/`, `admin/`), `templates/`, `static/`, and shared modules (`models.py`, `extensions.py`, `security.py`, `tenancy.py`).
- app.py: WSGI entry using `create_app()`.
- migrations/: Alembic migration scripts.
- tests/: Pytest suite with fixtures (`conftest.py`).
- instance/: Local instance data (e.g., SQLite DB).
- assets: Tailwind sources in `app/static/css/`.

## Build, Test, and Development Commands
- Install: `pip install -r requirements.txt` and `npm install`.
- Dev server: `make dev` (runs `flask --app app.py run`).
- CSS (watch): `npm run build-css` (Tailwind watch to `app/static/css/app.css`).
- CSS (one-off): `make build-css`.
- DB migrate: `make migrate` then `flask --app app.py db upgrade`.
- Seed demo: `python manage.py seed_demo` (optional).
- Test: `make test` or `pytest`.
- Lint/format: `make lint` (`ruff check .`) and `make fmt` (`ruff format .`).
- Prod serve: `make run` (`gunicorn -w 4 'app:app'`).

## Coding Style & Naming Conventions
- Python: 4-space indent, prefer type hints for new code; run `ruff check .` and `ruff format .` before pushing.
- Names: `snake_case` for modules/functions, `PascalCase` for models, `CONSTANT_CASE` for constants. Blueprint routes live under their module.
- Templates: `.html` in `app/templates/`; static under `app/static/`.

## Testing Guidelines
- Framework: Pytest with in-memory SQLite (configured in `tests/conftest.py`).
- Location: Place tests in `tests/` named `test_*.py`.
- Running: `pytest -q` or `make test`.
- Prefer fixture-driven tests; use the `client` fixture for authenticated flows and multi-tenant scoping.

## Commit & Pull Request Guidelines
- Commits: Use concise, imperative messages (e.g., "Add org scoping to files"). Conventional Commits optional; not enforced in history.
- PRs: Include purpose, linked issues, and testing notes. Add screenshots/GIFs for UI/template changes. Call out DB/schema changes and include Alembic migrations.

## Security & Configuration Tips
- Env: Copy `.env.example` to `.env`. For production set `DATABASE_URL`, `SECRET_KEY`, and enable secure cookies (`SESSION_COOKIE_SECURE=1`, `REMEMBER_COOKIE_SECURE=1`).
- Uploads: `MAX_UPLOAD_MB` controls limits. Rate limiting via `Flask-Limiter` is enabled.
