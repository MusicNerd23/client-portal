# Project Overview

This project is a multi-tenant client portal. Each company ("Organization") has an isolated workspace. Users only see data for their organization. JusB Solutions staff have a global "JusB Admin" view.

The MVP features include:
*   Secure login
*   Organization dashboard
*   Message threads
*   File exchange
*   Tasks/notes
*   Activity log

## Technologies

*   **Backend:** Python 3.12, Flask, SQLAlchemy, Flask-Login, Flask-WTF/CSRF, Alembic
*   **Database:** PostgreSQL
*   **Frontend:** Tailwind CSS (JIT), HTML/Jinja templates
*   **Authentication:** Email + password (hashing), session auth
*   **Storage:** Local `/uploads` for development, with an abstraction class for S3/Backblaze in production.
*   **Testing:** pytest
*   **Tooling:** uv/venv or pip-tools, ruff + black, pre-commit, dotenv, Makefile
*   **Server:** gunicorn

## Development Conventions

*   **Code Style:** `ruff` and `black` will be used for linting and formatting, enforced with a `pre-commit` hook.
*   **Testing:** `pytest` will be used for testing.
*   **Makefile:** A `Makefile` will provide tasks for common development operations like running the development server, linting, formatting, testing, and building CSS.
*   **Database Migrations:** `Alembic` will be used for database migrations.
*   **Environment Variables:** `dotenv` will be used for managing environment variables.

## Data Model

The database will have the following tables:

*   `Organization(id, name, slug, created_at)`
*   `User(id, org_id->Organization, email UNIQUE, password_hash, role in {"client","client_admin","jusb_admin"}, is_active, created_at)`
*   `Thread(id, org_id, title, created_at, created_by->User)`
*   `Message(id, thread_id->Thread, author_id->User, body TEXT, attachments JSONB, created_at)`
*   `File(id, org_id, uploader_id->User, filename, path, mime, size, created_at)`
*   `Task(id, org_id, title, description, status {"open","in_progress","done"}, assignee_id->User NULL, due_date NULL, created_at)`
*   `Activity(id, org_id, actor_id->User, action, target_type, target_id, created_at)`

## Security

*   **Tenancy:** Every table that holds tenant data will include an `org_id`. All queries will be scoped by `org_id`.
*   **Authentication:** Passwords will be hashed using `werkzeug.security`.
*   **CSRF:** `Flask-WTF` will be used for CSRF protection.
*   **Session Cookies:** Session cookies will be configured with `HttpOnly`, `Secure`, and `SameSite=Lax`.
*   **File Uploads:** File uploads will be validated for size and MIME type.
*   **Rate Limiting:** `Flask-Limiter` will be used to rate limit login attempts and file uploads.
