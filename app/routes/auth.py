from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, User
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        email = request.form['email']

        if not username or not password or not role or not email:
            flash('Please fill out all fields')
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password_hash=generate_password_hash(password), role=role, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')
