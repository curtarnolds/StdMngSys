from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, User
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import UserRegistrationForm
from werkzeug.security import generate_password_hash
from app.services.auth_service import register_user


bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    registration_form = UserRegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        role = registration_form.role.data
        email = registration_form.email.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        new_user = register_user(username=username, password_hash=password, role=role, email=email)
        if new_user:
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')
