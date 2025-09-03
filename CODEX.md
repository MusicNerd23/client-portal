Brandon — here’s the killer prompt you can paste into Gemini CLI to generate the MVP client portal project.

⸻

Prompt for Gemini CLI

You are a senior full-stack engineer with 30+ years of experience. Generate a production-grade multi-tenant client portal built with:
	•	Backend: Python 3.12, Flask, SQLAlchemy, Flask-Login, Flask-WTF/CSRF, Alembic
	•	DB: PostgreSQL
	•	Frontend: Tailwind CSS (JIT), HTML/Jinja templates, dark mode toggle
	•	Auth: email + password (hashing), session auth (no JWT in MVP), optional “remember me”
	•	Storage: local /uploads for dev; abstraction class ready for S3/Backblaze in prod
	•	Tests: pytest
	•	Tooling: uv/venv or pip-tools, ruff + black, pre-commit, dotenv, Makefile tasks
	•	Server: gunicorn + (nginx config example in docs)
	•	Git: initialize repo, meaningful commits, .gitignore, basic CI (GitHub Actions) running lint+tests
	•	Licensing: MIT

Business goal

Create a client portal where each company (“Organization”) has an isolated workspace. Users only see data for their org. JusB Solutions staff have a global “JusB Admin” view. MVP features: secure login, org dashboard, message threads, file exchange, tasks/notes, activity log.

Visual design
	•	Modern, clean UI (Apple-like minimalism).
	•	Light/dark modes with Tailwind dark class strategy.
	•	Color palette:
	•	Primary: blue-600 / blue-700
	•	Background: white (light) / slate-900 (dark)
	•	Accents: slate/gray for UI chrome; success emerald, warning amber, danger rose
	•	Typography: system font stack.
	•	Components: sticky top nav, left sidebar, cards, badges, modals, dropzones, toasts.

Security & tenancy (NON-NEGOTIABLE)
	•	Every table that holds tenant data includes org_id.
	•	All queries must be scoped by org_id.
	•	Route decorators to enforce role + org scoping.
	•	CSRF enabled, strong session cookies: HttpOnly, Secure, SameSite=Lax.
	•	Passwords: werkzeug.security (generate/check hash).
	•	File uploads are saved under /uploads/{org_slug}/... and validated (size, mime allowlist).
	•	Add Flask-Limiter with sane defaults (login attempts, file upload).

Data model (MVP)

Organization(id, name, slug, created_at)
User(id, org_id->Organization, email UNIQUE, password_hash, role in {"client","client_admin","jusb_admin"}, is_active, created_at)
Thread(id, org_id, title, created_at, created_by->User)
Message(id, thread_id->Thread, author_id->User, body TEXT, attachments JSONB, created_at)
File(id, org_id, uploader_id->User, filename, path, mime, size, created_at)
Task(id, org_id, title, description, status {"open","in_progress","done"}, assignee_id->User NULL, due_date NULL, created_at)
Activity(id, org_id, actor_id->User, action, target_type, target_id, created_at)

Roles & permissions
	•	client: only own org, can post messages, upload files, create tasks.
	•	client_admin: client + manage users in org.
	•	jusb_admin: global view, switch orgs, impersonate with audit log.

Project structure

client-portal/
  app.py
  config.py
  manage.py
  requirements.txt or pyproject.toml
  .env.example
  Makefile
  README.md
  .gitignore
  alembic.ini
  migrations/
  app/
    __init__.py
    extensions.py
    models.py
    security.py
    tenancy.py
    auth/
      routes.py
      forms.py
    org/
      routes.py
    threads/
      routes.py
      forms.py
    files/
      routes.py
      forms.py
    tasks/
      routes.py
      forms.py
    admin/
      routes.py
    templates/
      base.html
      components/
    static/
      css/
        input.css
        app.css
      js/
        app.js
  tailwind.config.js
  postcss.config.js
  package.json
  tests/
    test_auth.py
    test_tenancy.py
    test_threads.py
    test_files.py
    test_tasks.py

Tailwind setup
	•	darkMode: 'class'
	•	Colors: blue, slate, emerald, amber, rose.
	•	Dark mode toggle saves to localStorage.

Key screens
	1.	Login
	2.	Org Dashboard
	3.	Threads & Messages
	4.	Files (upload, list)
	5.	Tasks (CRUD, status)
	6.	Admin (JusB)
	7.	Profile

Routing & scoping
	•	Clients: current_user.org
	•	JusB admins: switch org via session admin_org_id.
	•	All queries filtered by org_id.

CLI & seeding
	•	init-db, create-superuser, seed-demo

Makefile tasks
	•	make dev, make lint, make fmt, make test, make build-css, make run, make migrate

Deliverables
	1.	Fully generated codebase.
	2.	Passing tests.
	3.	Seed script with sample orgs (Acme, Contoso, JusB admin).
	4.	Screens with Tailwind.
	5.	README + Makefile.

Stretch (scaffold only)
	•	Password reset via email token.
	•	Notifications.
	•	S3 storage stub.

Start now. Output the complete project with all files, then a concise “How to run (dev)” section and first 10 Git commit messages.