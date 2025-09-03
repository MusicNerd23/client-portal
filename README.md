# Client Portal

This is a multi-tenant client portal.

## How to run (dev)

1.  Install dependencies: `pip install -r requirements.txt` and `npm install`
2.  Create a `.env` file from `.env.example` and fill in the values.
3.  Initialize the database: `flask db init` and `flask db migrate` and `flask db upgrade`
4.  Run the development server: `make dev`
