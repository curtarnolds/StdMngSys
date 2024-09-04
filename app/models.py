"""Database Table Definitions"""
from datetime import date, datetime, timezone
from flask_login import UserMixin
from app import db, login


class Person(UserMixin):
    """Define the User Table."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    image = db.Column(db.String(100))
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    # relationships
    sent_feedbacks = db.relationship(
        "Feedback", foreign_keys="Feeback.author_id", backref='author',
        lazy=True)
    received_feedbacks = db.relationship(
        "Feedback", foreign_keys="Feeback.recipient_id", backref='recipient',
        lazy=True)


# Association table for the many-to-many relationship
student_course = db.Table('student_course',
                          db.Column('student_id', db.Integer, db.ForeignKey(
                              'student.id'), primary_key=True),
                          db.Column('course_id', db.Integer, db.ForeignKey(
                              'course.id'), primary_key=True)
                          )


staff_course = db.Table('staff_course',
                        db.Column('staff_id', db.Integer, db.ForeignKey(
                            'staff.id'), primary_key=True),
                        db.Column('course_id', db.Integer, db.ForeignKey(
                            'course.id'), primary_key=True)
                        )


class Staff(Person, db.Model):
    staff_id = db.Column(db.String(10), unique=True, nullable=False)
    date_employed = db.Column(db.DateTime, nullable=False, default=date.today)
    role = db.Column(db.String(20), nullable=False)

    courses = db.relationship(
        'Course', secondary=staff_course, backref=db.backref(
            'staff', lazy='dynamic'))


class Student(Person, db.Model):
    """Define the Student Table."""
    index_number = db.Column(db.String(20), unique=True, nullable=False)
    date_admitted = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    year = db.Column(db.Integer, nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    hall_id = db.Column(db.Integer, db.ForeignKey("hall.id"))

    # Define the relationship to Course, linking it via the association table
    courses = db.relationship(
        'Course', secondary=student_course, backref=db.backref(
            'students', lazy='dynamic'))


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    head = db.Column(db.Integer, db.ForeignKey("staff.id"))
    programs = db.relationship('Program', backref='department')
    students = db.relationship('Student', backref='department')
    members = db.relationship('Staff', backref='department')
    courses = db.relationship('Course', backref='department')


program_courses = db.Table('program_courses',
                           db.Column('program_id', db.Integer, db.ForeignKey(
                               'program.id'), primary_key=True),
                           db.Column('course_id', db.Integer, db.ForeignKey(
                               'course.id'), primary_key=True)
                           )


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    duration = db.Column(db.Integer, nullable=False)
    courses = db.relationship(
        "Course", secondary=program_courses, backref=db.backref("programs"))
    students = db.relationship("Student", backref="program", lazy=True)


class Course(db.Model):
    """Define the Course Table."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    enrollment = db.relationship("Enrollment", backref='course')


class Enrollment(db.Model):
    """Define the Enrollment Table to handle Enrollments"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)

    student = db.relationship(
        "Student", backref=db.backref('enrollments', lazy=True))
    course = db.relationship(
        "Course", backref=db.backref('enrollments', lazy=True))


class Hall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship("Student", backref="hall", lazy=True)


class Grade(db.Model):
    """Define the Grade Table to store student grades"""
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey(
        'enrollment.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    quiz = db.Column(db.Numeric(5, 2), default=0)
    assignment = db.Column(db.Numeric(5, 2), default=0)
    midsem = db.Column(db.Numeric(5, 2), default=0)
    exam = db.Column(db.Numeric(5, 2), default=0)
    grade = db.Column(db.String(2))

    enrollment = db.relationship(
        "Enrollment", backref=db.backref('grades', lazy=True))

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


class Feedback(db.Model):
    """Define the Feedback table to store feedback"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('person.id'), nullable=False)
    recipient_id = db.Column(
        db.Integer, db.ForeignKey('person.id'), nullable=False)


@login.user_loader
def load_user(user_id):
    return Person.query.get(int(id))
