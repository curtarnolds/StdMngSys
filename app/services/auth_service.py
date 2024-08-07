from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from app.models import User
from app import db


def register_user(username, password, role, email):
    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash,
                role=role, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def user_login(email, password, remember):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=remember)
    return False
