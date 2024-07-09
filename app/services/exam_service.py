from app.models import Exam, Question, Answer, Response
from app import db

def create_exam(course_id, exam_name, exam_date):
    exam = Exam(course_id=course_id, exam_name=exam_name, exam_date=exam_date)
    db.session.add(exam)
    db.session.commit()
    return exam

def get_exam(exam_id):
    return Exam.query.get(exam_id)

def update_exam(exam_id, exam_name, exam_date):
    exam = Exam.query.get(exam_id)
    exam.exam_name = exam_name
    exam.exam_date = exam_date
    db.session.commit()
    return exam

def delete_exam(exam_id):
    exam = Exam.query.get(exam_id)
    db.session.delete(exam)
    db.session.commit()

def create_question(exam_id, question_text):
    question = Question(exam_id=exam_id, question_text=question_text)
    db.session.add(question)
    db.session.commit()
    return question

def create_answer(question_id, answer_text, is_correct):
    answer = Answer(question_id=question_id, answer_text=answer_text, is_correct=is_correct)
    db.session.add(answer)
    db.session.commit()
    return answer

def record_response(student_id, question_id, selected_answer_id):
    response = Response(student_id=student_id, question_id=question_id, selected_answer_id=selected_answer_id)
    db.session.add(response)
    db.session.commit()
    return response
