from app.models import Enrollment
from app import db
from datetime import date


def enroll_student_in_courses(student_id, course_ids):
    """Enroll a student in courses."""
    for course_id in course_ids:
        enrollment = Enrollment(
            student_id=student_id, course_id=course_id,
            enrollment_date=date.today)
        db.session.add(enrollment)
    db.session.commit()
