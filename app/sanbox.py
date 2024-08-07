from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services import course_service
from app.models import Course
from app import db, login


class Course(db.Model):
    """Define the Course Table."""
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(15), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    enrollment = db.Column(db.Integer, nullable=False, default=0)
