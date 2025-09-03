from flask import Flask
from config import Config
from .extensions import db, login_manager, migrate
from .models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

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

    from .admin.routes import admin
    app.register_blueprint(admin, url_prefix='/admin')

    @app.route('/')
    def index():
        return '<h1>Client Portal</h1>'

    return app
