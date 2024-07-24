from flask_wtf import FlaskForm
from wtforms import RadioField, PasswordField, SubmitField, BooleanField,\
      TextAreaField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class UserRegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = RadioField('Role', validators=[DataRequired()], choices=[('Teacher', 'teacher'), ('Student', 'student')])
    password = PasswordField('Enter Password', validators=[DataRequired()], choices=['Teacher', 'Student'])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
