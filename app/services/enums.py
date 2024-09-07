from enum import Enum
"""
This module contains the enumeration classes used in the student management
system.

Enumerations:
- `StaffRole`: Enumerates the roles of staff members.
- `Sex`: Enumerates the possible sexes.
- `SchoolYear`: Enumerates the different school years.
- `Semester`: Enumerates the semesters.
- `StudentStatus`: Enumerates the possible student statuses.
- `ExamType`: Enumerates the types of exams.
- `QuestionType`: Enumerates the types of questions.

Each enumeration class defines a set of named constants that represent the
possible values for the corresponding attribute.

Example usage:
    staff_role = StaffRole.TEACHER
    sex = Sex.MALE
    school_year = SchoolYear.FRESHMAN
    semester = Semester.ONE
    student_status = StudentStatus.ENROLLED
    exam_type = ExamType.MIDTERM
    question_type = QuestionType.MCQ
"""


class StaffRole(Enum):
    """
    Enum class representing the roles of staff members.

    Attributes:
        TEACHER (str): Represents a teacher role.
        ADMIN (str): Represents an administrative role.
        STAFF (str): Represents a general staff role.
    """
    TEACHER = 'Teacher'
    ADMIN = 'Admin'
    STAFF = 'Staff'


class Sex(Enum):
    """
    Enum class representing the sexes.

    Attributes:
        MALE (str): Represents a male individual.
        FEMALE (str): Represents a female individual.
        OTHER (str): Represents a non-binary or other gender identity.
    """
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class SchoolYear(Enum):
    """
    Enum class representing the different school years.

    Attributes:
        FRESHMAN (str): Represents the freshman year (1st year).
        SOPHOMORE (str): Represents the sophomore year (2nd year).
        JUNIOR (str): Represents the junior year (3rd year).
        SENIOR (str): Represents the senior year (4th year).
    """
    FRESHMAN = "freshman"
    SOPHOMORE = "sophomore"
    JUNIOR = "junior"
    SENIOR = "senior"


class Semester(Enum):
    """
    Enum class representing the semesters.

    Attributes:
        ONE (int): Represents the first semester.
        TWO (int): Represents the second semester.
    """
    ONE = 1
    TWO = 2


class StudentStatus(Enum):
    """
    Enum class representing the status of a student.

    Attributes:
        ENROLLED (str): The student is currently enrolled.
        GRADUATED (str): The student has graduated.
        DROPPED_OUT (str): The student has dropped out.
        SUSPENDED (str): The student is currently suspended.
        DISMISSED (str): The student has been dismissed from the institution.
    """
    ENROLLED = "enrolled"
    GRADUATED = "graduated"
    DROPPED_OUT = "dropped_out"
    SUSPENDED = "suspended"
    DISMISSED = "dismissed"


class ExamType(Enum):
    """
    Enum class representing different types of exams.

    Attributes:
        MIDTERM (str): Represents a midterm exam.
        FINAL (str): Represents a final exam.
        QUIZ (str): Represents a quiz.
        ASSIGNMENT (str): Represents an assignment.
    """
    MIDTERM = "midterm"
    FINAL = "final"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"


class QuestionType(Enum):
    """
    Enum class representing different types of questions in exams.

    Attributes:
        MCQ (str): Represents a multiple-choice question.
        ESSAY (str): Represents an essay question.
        TRUE_FALSE (str): Represents a true/false question.
        FILL_IN_THE_BLANK (str): Represents a fill-in-the-blank question.
        MULTIPLE_ANSWER (str): Represents a multiple-answer question.
    """
    MCQ = "mcq"
    ESSAY = "essay"
    TRUE_FALSE = "true_false"
    FILL_IN_THE_BLANK = "fill_in_the_blank"
    MULTIPLE_ANSWER = "multiple_answer"
