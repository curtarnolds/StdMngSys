from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services import student_service
from app.models import Student
from app.forms import CreateStudentForm


bp = Blueprint('students', __name__)


@bp.route('/students')
@login_required
def list_students():
    students = Student.query.all()
    return render_template('students/list.html', students=students)


@bp.route('/students/<int:id>')
@login_required
def detail_student(id):
    student = student_service.get_student(id)
    return render_template('students/detail.html', student=student)


@bp.route('/students/create', methods=['GET', 'POST'])
@login_required
def create_student():
    form = CreateStudentForm()
    if form.validate_on_submit():
        # Process the form data (e.g., save to database)
        user_id = form.user_id.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        date_of_birth = form.date_of_birth.data
        gender = form.gender.data
        address = form.address.data
        student_index_number = form.student_index_number.data
        student_service.create_student(user_id, first_name, last_name,
                                       date_of_birth, gender, address,
                                       student_index_number)
        return redirect(url_for('students.list_students'))
    return render_template('students/create.html', form=form)


@bp.route('/students/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_student(id):
    student = student_service.get_student(id)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        address = request.form['address']
        student_index_number = request.form['student_index_number']
        student_service.update_student(
            id, first_name, last_name, date_of_birth, gender, address,
            student_index_number)
        return redirect(url_for('students.list_students'))
    return render_template('students/update.html', student=student)


@bp.route('/students/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    student_service.delete_student(id)
    return redirect(url_for('students.list_students'))
