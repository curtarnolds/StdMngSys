from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))
#   return render_template('index.html')
