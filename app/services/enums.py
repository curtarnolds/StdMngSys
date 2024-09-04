from enum import Enum
"""
This module contains the enumeration classes used in the student management system.

- `StaffRole`: Enumerates the roles of staff members.
- `Sex`: Enumerates the possible sexes.
- `SchoolYear`: Enumerates the different school years.
- `Semester`: Enumerates the semesters.
- `StudentStatus`: Enumerates the possible student statuses.
- `ExamType`: Enumerates the types of exams.

Each enumeration class defines a set of named constants that represent the possible values for the corresponding attribute.

Example usage:
    staff_role = StaffRole.TEACHER
    sex = Sex.MALE
    school_year = SchoolYear.FRESHMAN
    semester = Semester.ONE
    student_status = StudentStatus.ENROLLED
    exam_type = ExamType.MIDTERM
"""


class StaffRole(Enum):
    TEACHER = 'Teacher'
    ADMIN = 'Admin'
    STAFF = 'Staff'


class Sex(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class SchoolYear(Enum):
    FRESHMAN = "freshman"
    SOPHOMORE = "sophomore"
    JUNIOR = "junior"
    SENIOR = "senior"


class Semester(Enum):
    ONE = 1
    TWO = 2


class StudentStatus(Enum):
    ENROLLED = "enrolled"
    GRADUATED = "graduated"
    DROPPED_OUT = "dropped_out"
    SUSPENDED = "suspended"
    DISMISSED = "dismissed"


class ExamType(Enum):
    MIDTERM = "midterm"
    FINAL = "final"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"


class QuestionType(Enum):
    MCQ = "mcq"
    ESSAY = "essay"
    TRUE_FALSE = "true_false"
    FILL_IN_THE_BLANK = "fill_in_the_blank"
    MULTIPLE_ANSWER = "multiple_answer"
