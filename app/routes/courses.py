from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services import course_service
from app.models import Course

bp = Blueprint('courses', __name__)


@bp.route('/courses')
@login_required
def list_courses():
    courses = Course.query.all()
    return render_template('courses/list.html', courses=courses)


@bp.route('/courses/<int:id>')
@login_required
def detail_course(id):
    course = course_service.get_course(id)
    return render_template('courses/detail.html', course=course)


@bp.route('/courses/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_description = request.form['course_description']
        credits = request.form['credits']
        course_service.create_course(course_name, course_description, credits)
        return redirect(url_for('courses.list_courses'))
    return render_template('courses/create.html')


@bp.route('/courses/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_course(id):
    course = course_service.get_course(id)
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_description = request.form['course_description']
        credits = request.form['credits']
        course_service.update_course(
            id, course_name, course_description, credits)
        return redirect(url_for('courses.list_courses'))
    return render_template('courses/update.html', course=course)


@bp.route('/courses/delete/<int:id>', methods=['POST'])
@login_required
def delete_course(id):
    course_service.delete_course(id)
    return redirect(url_for('courses.list_courses'))
