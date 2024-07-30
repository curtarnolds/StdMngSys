from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, User
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import UserRegistrationForm, UserLoginForm
from werkzeug.security import generate_password_hash
from app.services.auth_service import register_user, user_login


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

        new_user = register_user(username=username, password_hash=password, role=role, email=email)
        if new_user:
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=registration_form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    user_login_form = UserLoginForm()
    if user_login_form.validate_on_submit():
        login = user_login(email=user_login_form.email.data,
                           password=user_login_form.password.data, remember=user_login_form.remember.data)
        if login:
            flash('Login successful!')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Login unsuccessful. Please check email or password')
    return render_template('auth/login.html', form=user_login_form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
