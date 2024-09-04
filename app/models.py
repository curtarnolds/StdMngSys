"""Database Table Definitions"""
from datetime import datetime
from flask_login import UserMixin
from app import db, login


class User(db.Model, UserMixin):
    """Define the User Table."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


# class Person(UserMixin):
#     """Define the Person class"""
#     id = db.Column(db.Integer, primary_key=True)
#     firstName = db.Column(db)


class Student(db.Model):
    """Define the Student Table."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    student_index_number = db.Column(
        db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    head = db.Column(db.Integer, db.ForeignKey("staff.id"))
    programs = db.relationship('Program', backref='department')
    students = db.relationship('Student', backref='department')
    members = db.relationship('Staff', backref='department')


class Course(db.Model):
    """Define the Course Table."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    # department = db.Column(db.Integer, db.ForeignKey(
    #     'department.id', name='fk_course_department'), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    year = db.Column(db.String(4), nullable=False)


class Enrollment(db.Model):
    """Define the Enrollment Table to handle Enrollments"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)


class Grade(db.Model):
    """Define the Grade Table to store student grades"""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id', name='fk_grade_course'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id', name='fk_grade_student'), nullable=False)
    year = db.Column(db.Date, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    quiz = db.Column(db.Integer, default=0)
    assignment = db.Column(db.Integer, default=0)
    midsem = db.Column(db.Integer, default=0)
    exam = db.Column(db.Integer, default=0)
    enrollment_id = db.Column(db.Integer, db.ForeignKey(
        'enrollment.id', name='fk_grade_enrollment'), nullable=False)
    grade = db.Column(db.String(2))

    course = db.relationship("Course", backref=db.backref('grades'), lazy=True)
    student = db.relationship(
        "Student", backref=db.backref('grades'), lazy=True)

    def get_total(self):
        return self.quiz + self.assignment + self.midsem + self.exam


class Notification(db.Model):
    """Define the Notification table to store user notifications"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Report(db.Model):
    """Define the Report table to store student reports"""
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.JSON)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)
    selected_answer_id = db.Column(
        db.Integer, db.ForeignKey('answer.id'), nullable=False)
    response_date = db.Column(db.DateTime, default=datetime.utcnow)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
