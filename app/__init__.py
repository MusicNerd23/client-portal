from flask import Flask
import os
from config import Config
from .extensions import db, login_manager, migrate, csrf, limiter
from .models import User
from sqlalchemy.exc import SQLAlchemyError

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Normalize relative SQLite URIs to absolute paths to avoid
    # "unable to open database file" when CWD varies.
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if isinstance(uri, str) and uri.startswith('sqlite:///') and not uri.startswith('sqlite:////'):
        rel_path = uri.replace('sqlite:///', '', 1)
        if not os.path.isabs(rel_path):
            project_root = os.path.dirname(app.root_path)
            abs_path = os.path.abspath(os.path.join(project_root, rel_path))
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{abs_path}"

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        try:
            return db.session.get(User, int(id))
        except SQLAlchemyError:
            # DB might not be initialized yet; treat as anonymous
            return None

    login_manager.login_view = 'auth.login'

    from .auth.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .org.routes import org
    app.register_blueprint(org, url_prefix='/org')

    from .threads.routes import threads
    app.register_blueprint(threads, url_prefix='/threads')

    from .files.routes import files
    app.register_blueprint(files, url_prefix='/files')

    from .tasks.routes import tasks
    app.register_blueprint(tasks, url_prefix='/tasks')

    from .tickets.routes import tickets
    app.register_blueprint(tickets, url_prefix='/tickets')

    from .admin.routes import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from .profile import profile
    app.register_blueprint(profile)

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('home.html')

    return app

# Re-export db for convenience (tests import `from app import db`).
