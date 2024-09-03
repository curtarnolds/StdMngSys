from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, logout_user
from app.forms import UserRegistrationForm, UserLoginForm
from app.services.auth_service import register_user, user_login
