"""
Database Table Definitions

This module contains the database table definitions used in the application.
It uses SQLAlchemy for ORM and Flask-Login for user session management.

Classes:
- Person: Abstract base class representing a user (either Staff or Student).
- Staff: Represents a staff member in the system.
- Student: Represents a student in the system.
- Department: Represents a department in the system.
- Program: Represents a program of study in the system.
- Course: Represents a course in the system.
- Enrollment: Handles the enrollment of a student in a course.
- Hall: Represents a hall of residence for students.
- Grade: Represents a grade of a student in a course.
- Exam: Represents an exam in a course.
- Question: Represents a question in an exam.
- Answer: Represents a possible answer to a question.
- Response: Represents a student’s response to a question.
- Feedback: Represents feedback exchanged between users.
- Notification: Represents notifications sent to users.
- Schedule: Represents a course schedule.
- Report: Represents a report related to students.
- Announcement: Represents system-wide announcements.

Functions:
- load_user: Loads a user from the database based on the given user ID.

Enums (imported from app.services.enums):
- ExamType: Enum to define types of exams.
- QuestionType: Enum to define types of questions.
- SchoolYear: Enum representing different years in the school system.
- Semester: Enum representing academic semesters.
- Sex: Enum representing the gender of users.
- StaffRole: Enum representing different roles of staff.
- StudentStatus: Enum representing the status of a student.
"""

from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import Enum as EnumType

from app import db, login
from app.services.enums import ExamType, QuestionType, SchoolYear, Semester, \
    Sex, UserRole, StudentStatus


class Person(UserMixin):
    """
    Represents a user in the system (either Staff or Student).

    Abstract base class containing common fields and relationships.

    Attributes:
    - id (int): Unique ID of the person.
    - first_name (str): First name of the person.
    - middle_name (str): Middle name of the person.
    - last_name (str): Last name of the person.
    - date_of_birth (date): Date of birth of the person.
    - sex (enum): Gender of the person (from the Sex enum).
    - image (str): URL of the person’s profile image.
    - password_hash (str): Hashed password for authentication.
    - email (str): Unique email address of the person.
    - address (str): Address of the person.
    - department_id (int): Foreign key to the person’s department.
    - sent_feedbacks (relationship): Feedbacks sent by the person.
    - received_feedbacks (relationship): Feedbacks received by the person.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    sex = db.Column(EnumType(Sex), nullable=False)
    image = db.Column(db.String(100))
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    role = db.Column(EnumType(UserRole), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    # relationships
    sent_feedbacks = db.relationship(
        "Feedback", foreign_keys="Feedback.author_id", backref='author',
        lazy=True)
    received_feedbacks = db.relationship(
        "Feedback", foreign_keys="Feedback.recipient_id", backref='recipient',
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
    """
    Represents a staff member in the system.

    Attributes:
    - staff_id (str): Unique ID for the staff member.
    - date_employed (datetime): Date when the staff member was employed.
    - role (enum): Role of the staff member (from StaffRole enum).
    - courses (relationship): Many-to-many relationship with courses.
    """
    staff_id = db.Column(db.String(10), unique=True, nullable=False)
    date_employed = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    courses = db.relationship(
        'Course', secondary='staff_course', backref=db.backref(
            'staff', lazy='dynamic'))


class Student(Person, db.Model):
    """
    Represents a student in the system.

    Attributes:
    - index_number (str): Unique index number of the student.
    - date_admitted (datetime): Date when the student was admitted.
    - status (enum): Status of the student (from StudentStatus enum).
    - year (enum): Year of study (from SchoolYear enum).
    - program_id (int): Foreign key to the student’s program.
    - hall_id (int): Foreign key to the student’s hall of residence.
    - courses (relationship): Many-to-many relationship with courses.
    """
    index_number = db.Column(db.String(20), unique=True, nullable=False)
    date_admitted = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    status = db.Column(EnumType(StudentStatus), nullable=False)
    year = db.Column(EnumType(SchoolYear), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    hall_id = db.Column(db.Integer, db.ForeignKey("hall.id"))

    courses = db.relationship(
        'Course', secondary='student_course', backref=db.backref(
            'students', lazy='dynamic'))


class Department(db.Model):
    """
    Represents a department in the system.

    Attributes:
    - id (int): Unique ID of the department.
    - name (str): Name of the department.
    - head (int): Foreign key to the staff member who is head of the
    department.
    - programs (relationship): Programs offered by the department.
    - students (relationship): Students belonging to the department.
    - members (relationship): Staff members in the department.
    - courses (relationship): Courses offered by the department.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    head = db.Column(db.Integer, db.ForeignKey("staff.id"))
    programs = db.relationship('Program', backref='department')
    students = db.relationship('Student', backref='department')
    members = db.relationship('Staff', backref='department')
    courses = db.relationship('Course', backref='department')


class Program(db.Model):
    """
    Represents a program of study in the system.

    Attributes:
    - id (int): Unique ID of the program.
    - name (str): Name of the program.
    - description (str): Description of the program.
    - department_id (int): Foreign key to the associated department.
    - duration (int): Duration of the program in semesters.
    - courses (relationship): Courses associated with the program.
    - students (relationship): Students enrolled in the program.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    duration = db.Column(db.Integer, nullable=False)  # in semesters
    courses = db.relationship(
        "Course", secondary='program_courses', backref=db.backref("programs"))
    students = db.relationship("Student", backref="program", lazy=True)


class Course(db.Model):
    """
    Represents a course in the system.

    Attributes:
    - id (int): Unique ID of the course.
    - name (str): Name of the course.
    - code (str): Code of the course.
    - department_id (int): Foreign key to the department offering the course.
    - credits (int): Number of credits for the course.
    - year (enum): Year of study when the course is offered (from SchoolYear
    enum).
    - semester (enum): Semester in which the course is offered (from Semester
    enum).
    - enrollment (relationship): Enrollment records for the course.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    year = db.Column(EnumType(SchoolYear), nullable=False)
    semester = db.Column(EnumType(Semester), nullable=False)
    enrollment = db.relationship("Enrollment", backref='course')


class Enrollment(db.Model):
    """
    Represents the enrollment of a student in a course.

    Attributes:
    - id (int): Unique ID of the enrollment.
    - student_id (int): Foreign key to the student.
    - course_id (int): Foreign key to the course.
    - enrollment_date (date): Date of the enrollment.
    """
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


# The rest of the models would follow a similar pattern for documentation
# consistency


class Hall(db.Model):
    """
    Represents a hall of residence for students.

    Attributes:
    - id (int): Unique ID of the hall.
    - name (str): Name of the hall.
    - students (relationship): Students residing in the hall.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship("Student", backref="hall", lazy=True)


class Grade(db.Model):
    """
    Represents a grade for a student in a course.

    Attributes:
    - id (int): Unique ID of the grade.
    - enrollment_id (int): Foreign key to the enrollment (student-course
      relation).
    - year (int): Academic year in which the grade was awarded.
    - semester (int): Academic semester in which the grade was awarded.
    - quiz (decimal): Quiz score.
    - assignment (decimal): Assignment score.
    - midsem (decimal): Mid-semester exam score.
    - exam (decimal): End-of-semester exam score.
    - grade (str): Final letter grade.

    Methods:
    - get_total(): Returns the total score by summing quiz, assignment, midsem,
      and exam.
    """
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
        """Returns the total score."""
        return self.quiz + self.assignment + self.midsem + self.exam


class Exam(db.Model):
    """
    Represents an exam in the system.

    Attributes:
    - id (int): Unique ID of the exam.
    - course_id (int): Foreign key to the associated course.
    - exam_name (str): Name of the exam.
    - due_date (datetime): Date by which the exam should be completed.
    - type (enum): Type of exam (from ExamType enum).
    - start_date (datetime): Start date of the exam.
    """
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(EnumType(ExamType), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)


class Question(db.Model):
    """
    Represents a question in an exam.

    Attributes:
    - id (int): Unique ID of the question.
    - exam_id (int): Foreign key to the associated exam.
    - type (enum): Type of the question (from QuestionType enum).
    - question_text (str): Text of the question.
    """
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    type = db.Column(EnumType(QuestionType), nullable=False)
    question_text = db.Column(db.Text, nullable=False)

    exam = db.relationship('Exam', backref='questions')


class Answer(db.Model):
    """
    Represents an answer to a question in an exam.

    Attributes:
    - id (int): Unique ID of the answer.
    - question_id (int): Foreign key to the associated question.
    - answer_text (str): Text of the answer.
    - is_correct (bool): Whether the answer is correct or not.
    """
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)


class Response(db.Model):
    """
    Represents a student’s response to a question in an exam.

    Attributes:
    - id (int): Unique ID of the response.
    - student_id (int): Foreign key to the student who provided the response.
    - question_id (int): Foreign key to the question being answered.
    - selected_answer_id (int): Foreign key to the answer selected by the
      student.
    - response_date (datetime): Date and time when the response was submitted.
    """
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)
    selected_answer_id = db.Column(
        db.Integer, db.ForeignKey('answer.id'), nullable=False)
    response_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class Feedback(db.Model):
    """
    Represents feedback given by one user to another.

    Attributes:
    - id (int): Unique ID of the feedback.
    - title (str): Title of the feedback.
    - content (str): Content of the feedback.
    - author_id (int): Foreign key to the person giving the feedback.
    - recipient_id (int): Foreign key to the person receiving the feedback.
    - created_at (datetime): Date and time when the feedback was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'person.id'), nullable=False)
    recipient_id = db.Column(
        db.Integer, db.ForeignKey('person.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class Notification(db.Model):
    """
    Represents a notification sent to a user.

    Attributes:
    - id (int): Unique ID of the notification.
    - user_id (int): Foreign key to the user receiving the notification.
    - title (str): Title of the notification.
    - message (str): Notification message content.
    - created_at (datetime): Date and time when the notification was created.
    - is_read (bool): Indicates if the notification has been read.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('Person', backref='notifications')


class Schedule(db.Model):
    """
    Represents the schedule for a course.

    Attributes:
    - id (int): Unique ID of the schedule.
    - course_id (int): Foreign key to the associated course.
    - day (str): Day of the week for the schedule.
    - start_time (time): Start time of the class.
    - end_time (time): End time of the class.
    - location (str): Location of the class.
    """
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    course = db.relationship('Course', backref='schedules')


class Report(db.Model):
    """
    Represents a report related to a student or other entities.

    Attributes:
    - id (int): Unique ID of the report.
    - report_type (str): Type of the report (e.g., academic, disciplinary).
    - generated_at (datetime): Date and time when the report was generated.
    - data (JSON): Report data in JSON format.
    """
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.JSON)


class Announcement(db.Model):
    """
    Represents an announcement in the system.

    Attributes:
    - id (int): Unique ID of the announcement.
    - target_id (int): Foreign key to the target person (if applicable).
    - title (str): Title of the announcement.
    - content (str): Content of the announcement.
    - author_id (int): Foreign key to the author of the announcement.
    - created_at (datetime): Date and time when the announcement was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'person.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    author = db.relationship('Person', backref='announcements')


@login.user_loader
def load_user(user_id):
    """
    Load a user from the database based on the given user ID.

    Parameters:
    - user_id (int): The ID of the user to load.

    Returns:
    - Person: The user object corresponding to the given ID, or None if no
      user is found.
    """
    return Person.query.get(int(user_id))
