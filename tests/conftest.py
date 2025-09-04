import pytest

from app import create_app
from app.extensions import db
from app.models import Organization, User


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        # Use in-memory SQLite for tests
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        # Disable CSRF to allow simple form posts in tests
        "WTF_CSRF_ENABLED": False,
        # Provide a deterministic secret key
        "SECRET_KEY": "test-secret-key",
    }

    app = create_app()
    app.config.update(test_config)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app, request):
    # Seed default user/org for most tests; skip for tenancy test which seeds its own
    if request.module.__name__ != "tests.test_tenancy":
        with app.app_context():
            org = Organization(name="Default Org", slug="default-org")
            db.session.add(org)
            db.session.commit()

            user = User(email="test@example.com", role="client", org_id=org.id)
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

    ctx = app.app_context()
    ctx.push()
    try:
        yield app.test_client()
    finally:
        ctx.pop()