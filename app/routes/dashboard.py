from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

bp = Blueprint('dashboard', __name__)


@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return redirect(url_for('dashboard.student_dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('dashboard.teacher_dashboard'))
    else:
        return redirect(url_for('main.index'))


@bp.route('/dashboard/student')
@login_required
def student_dashboard():
    return render_template('dashboard/student.html')


@bp.route('/dashboard/teacher')
@login_required
def teacher_dashboard():
    return render_template('dashboard/teacher.html')
