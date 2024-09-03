from flask_wtf import FlaskForm
from wtforms import RadioField, PasswordField, SubmitField, BooleanField, \
    StringField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from app.models import User


class UserRegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = RadioField('Role', validators=[DataRequired()], choices=[
                      ('teacher', 'Teacher'), ('student', 'Student')],
                      default='student')
    password = PasswordField('Enter Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Check if username is taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one')

    def validate_email(self, email):
        """Check if email is taken."""
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is taken. Please choose a different one')


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CreateStudentForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
                         ('male', 'Male'), ('female', 'Female')],
                         default='male')
    address = StringField('Address')
    student_index_number = StringField(
        'Student Index Number', validators=[DataRequired()])
