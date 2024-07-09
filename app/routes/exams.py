from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services import exam_service
from app.models import Exam, Question, Answer

bp = Blueprint('exams', __name__)

@bp.route('/exams')
@login_required
def list_exams():
    exams = Exam.query.all()
    return render_template('exams/list.html', exams=exams)

@bp.route('/exams/<int:id>')
@login_required
def detail_exam(id):
    exam = exam_service.get_exam(id)
    questions = Question.query.filter_by(exam_id=id).all()
    return render_template('exams/detail.html', exam=exam, questions=questions)

@bp.route('/exams/create', methods=['GET', 'POST'])
@login_required
def create_exam():
    if request.method == 'POST':
        course_id = request.form['course_id']
        exam_name = request.form['exam_name']
        exam_date = request.form['exam_date']
        exam_service.create_exam(course_id, exam_name, exam_date)
        return redirect(url_for('exams.list_exams'))
    return render_template('exams/create.html')

@bp.route('/exams/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_exam(id):
    exam = exam_service.get_exam(id)
    if request.method == 'POST':
        exam_name = request.form['exam_name']
        exam_date = request.form['exam_date']
        exam_service.update_exam(id, exam_name, exam_date)
        return redirect(url_for('exams.list_exams'))
    return render_template('exams/update.html', exam=exam)

@bp.route('/exams/delete/<int:id>', methods=['POST'])
@login_required
def delete_exam(id):
    exam_service.delete_exam(id)
    return redirect(url_for('exams.list_exams'))

@bp.route('/exams/<int:exam_id>/questions/create', methods=['GET', 'POST'])
@login_required
def create_question(exam_id):
    if request.method == 'POST':
        question_text = request.form['question_text']
        exam_service.create_question(exam_id, question_text)
        return redirect(url_for('exams.detail_exam', id=exam_id))
    return render_template('exams/create_question.html')

@bp.route('/exams/<int:exam_id>/questions/<int:question_id>/answers/create', methods=['GET', 'POST'])
@login_required
def create_answer(exam_id, question_id):
    if request.method == 'POST':
        answer_text = request.form['answer_text']
        is_correct = request.form['is_correct'] == 'true'
        exam_service.create_answer(question_id, answer_text, is_correct)
        return redirect(url_for('exams.detail_exam', id=exam_id))
    return render_template('exams/create_answer.html', question_id=question_id)
