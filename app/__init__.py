'''App Initialiazation file'''
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.services import errors
from config import Config
import secrets



db = SQLAlchemy()
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
    # session['csrf_token'] = token

    from app.routes import auth, students, courses, grades, notifications, exams, main, dashboard
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


    return app
