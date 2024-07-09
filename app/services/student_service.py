from app.models import Student
from app import db


def create_student(user_id, first_name, last_name, date_of_birth,
                   gender, address, student_index_number):
    student = Student(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        address=address,
        student_index_number=student_index_number
    )
    db.session.add(student)
    db.session.commit()
    return student


def get_student(student_id):
    return Student.query.get(student_id)


def update_student(student_id, first_name, last_name, date_of_birth, gender, address, student_index_number):
    student = Student.query.get(student_id)
    student.first_name = first_name
    student.last_name = last_name
    student.date_of_birth = date_of_birth
    student.gender = gender
    student.address = address
    student.student_index_number = student_index_number
    db.session.commit()
    return student


def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
