"""
This module contains the forms used in the student management system
application.

The forms in this module are used for user registration, login, and data entry,
ensuring appropriate validation for fields such as email, password, and other
user-related information.

Classes:
    - BasePersonForm: A base form used to capture the common fields of a person,
      including names, date of birth, sex, and role.
    - StaffRegistrationForm: Inherits from BasePersonForm and includes fields
      specific to staff registration, such as staff ID and employment date.
    - StudentRegistrationForm: Inherits from BasePersonForm and includes fields
      specific to student registration, such as index number, program, and year.
    - StudentLoginForm: A form for students to log in, requiring an index number
      and password.
    - StaffLoginForm: A form for staff to log in, requiring a staff ID and
      password.
"""


from typing import Optional

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, \
    StringField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.services.enums import SchoolYear, Sex, StudentStatus, UserRole
from wtforms.validators import Regexp


class BasePersonForm(FlaskForm):
    """
    Form class for creating a base person.

    Attributes:
        first_name (StringField): Field for entering the first name of the
          person.
        middle_name (StringField): Field for entering the middle name of the
          person (optional).
        last_name (StringField): Field for entering the last name of the
          person.
        date_of_birth (DateField): Field for entering the date of birth of the
          person.
        sex (SelectField): Field for selecting the sex of the person.
        email (StringField): Field for entering the email address of the
          person.
        address (TextAreaField): Field for entering the address of the person.
        image (StringField): Field for entering the image URL of the person.
        password (PasswordField): Field for entering the password of the
          person.
        confirm_password (PasswordField): Field for confirming the password of
          the person.
        role (SelectField): Field for selecting the role of the person.
        department_id (StringField): Field for entering the department ID of
          the person.
        submit (SubmitField): The submit button for the form.
    """
    first_name = StringField('First Name', validators=[
                             DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[
                              Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[
                            DataRequired(), Length(max=50)])
    date_of_birth = DateField(
        'Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[(sex.value, sex.name)
                      for sex in Sex], validators=[DataRequired()])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(max=100)])
    address = TextAreaField('Address', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w])[A-Za-z\d\S]{8,}$',
               message='Password must contain at least 8 characters, including\
               at least one uppercase letter, one lowercase letter, one digit,\
                and one special character.')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
                       (role.value, role.name) for role in UserRole],
                       validators=[DataRequired()])
    department_id = StringField('Department ID', validators=[DataRequired()])
    submit = SubmitField('Register')


class StaffRegistrationForm(BasePersonForm):
    """
    Form for registering staff members.

    Attributes:
        staff_id (StringField): Field for entering staff ID.
        date_employed (DateField): Field for entering date of employment.

    """
    staff_id = StringField('Staff ID', validators=[
                           DataRequired(), Length(max=10)])
    date_employed = DateField(
        'Date Employed', format='%Y-%m-%d', validators=[DataRequired()])


class StudentRegistrationForm(BasePersonForm):
    """
    Form for registering a student.

    Attributes:
        index_number (StringField): Field for entering the index number of the
          student.
        date_admitted (DateField): Field for entering the date the student was
          admitted.
        status (SelectField): Field for selecting the status of the student.
        year (SelectField): Field for selecting the year of the student.
        program_id (StringField): Field for entering the program ID of the
          student.
        hall_id (StringField): Field for entering the hall ID of the student.
    """
    index_number = StringField('Index Number', validators=[
                               DataRequired(), Length(max=20)])
    date_admitted = DateField(
        'Date Admitted', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[(
        status.value, status.name) for status in StudentStatus],
        validators=[DataRequired()])
    year = SelectField('Year', choices=[
                       (year.value, year.name) for year in SchoolYear],
                       validators=[DataRequired()])
    program_id = StringField('Program ID', validators=[DataRequired()])
    hall_id = StringField('Hall ID', validators=[DataRequired()])


class StudentLoginForm(FlaskForm):
    """
    Represents a form for student login.

    Attributes:
        index_number (StringField): The index number of the student.
        password (PasswordField): The password of the student.
        remember (BooleanField): Indicates whether to remember the login.
        submit (SubmitField): The submit button for the form.
    """
    index_number = StringField('Index Number', validators=[DataRequired])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class StaffLoginForm(FlaskForm):
    """
    Form class for staff login.

    Attributes:
        staff_id (StringField): Field for staff ID.
        password (PasswordField): Field for password.
        remember (BooleanField): Field for remember me option.
        submit (SubmitField): The submit button for the form.
    """
    staff_id = StringField('Staff ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
