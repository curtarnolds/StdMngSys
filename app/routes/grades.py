from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services import grade_service
from app.models import Grade

bp = Blueprint('grades', __name__)


@bp.route('/grades')
@login_required
def list_grades():
    grades = Grade.query.all()
    return render_template('grades/list.html', grades=grades)


@bp.route('/grades/<int:id>')
@login_required
def detail_grade(id):
    grade = grade_service.get_grade(id)
    return render_template('grades/detail.html', grade=grade)


@bp.route('/grades/create', methods=['GET', 'POST'])
@login_required
def create_grade():
    if request.method == 'POST':
        enrollment_id = request.form['enrollment_id']
        grade = request.form['grade']
        grade_service.create_grade(enrollment_id, grade)
        return redirect(url_for('grades.list_grades'))
    return render_template('grades/create.html')


@bp.route('/grades/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_grade(id):
    grade = grade_service.get_grade(id)
    if request.method == 'POST':
        new_grade = request.form['grade']
        grade_service.update_grade(id, new_grade)
        return redirect(url_for('grades.list_grades'))
    return render_template('grades/update.html', grade=grade)


@bp.route('/grades/delete/<int:id>', methods=['POST'])
@login_required
def delete_grade(id):
    grade_service.delete_grade(id)
    return redirect(url_for('grades.list_grades'))
