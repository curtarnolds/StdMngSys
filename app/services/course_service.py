from app.models import Course
from app import db

def create_course(course_name, course_description, credits):
    course = Course(course_name=course_name, course_description=course_description, credits=credits)
    db.session.add(course)
    db.session.commit()
    return course

def get_course(course_id):
    return Course.query.get(course_id)

def update_course(course_id, course_name, course_description, credits):
    course = Course.query.get(course_id)
    course.course_name = course_name
    course.course_description = course_description
    course.credits = credits
    db.session.commit()
    return course

def delete_course(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
