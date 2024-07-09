from app.models import Grade
from app import db

def create_grade(enrollment_id, grade):
    grade_entry = Grade(enrollment_id=enrollment_id, grade=grade)
    db.session.add(grade_entry)
    db.session.commit()
    return grade_entry

def get_grade(grade_id):
    return Grade.query.get(grade_id)

def update_grade(grade_id, grade):
    grade_entry = Grade.query.get(grade_id)
    grade_entry.grade = grade
    db.session.commit()
    return grade_entry

def delete_grade(grade_id):
    grade_entry = Grade.query.get(grade_id)
    db.session.delete(grade_entry)
    db.session.commit()
