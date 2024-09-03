'''App Initialiazation file'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # noqa
from flask_login import LoginManager
from app.services import errors  # noqa
from config import Config
import secrets  # noqa
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # token = secrets.token_hex(16)
    # app.session['csrf_token'] = token

    from app.routes import auth, students, courses, grades, notifications, \
        exams, main, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(grades.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(notifications.bp)
    app.register_blueprint(exams.bp)
    app.register_blueprint(dashboard.bp)

    # app.register_error_handler(405, errors.wrong_login)
    # @app.errorhandler(404)
    # def wrong_login(e):
    #     return 'Test', 404
    app.app_context().push()
    return app
