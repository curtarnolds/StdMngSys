from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services import notification_service
from app.models import Notification

bp = Blueprint('notifications', __name__)

@bp.route('/notifications')
@login_required
def list_notifications():
    notifications = Notification.query.all()
    return render_template('notifications/list.html', notifications=notifications)

@bp.route('/notifications/<int:id>')
@login_required
def detail_notification(id):
    notification = notification_service.get_notification(id)
    return render_template('notifications/detail.html', notification=notification)

@bp.route('/notifications/create', methods=['GET', 'POST'])
@login_required
def create_notification():
    if request.method == 'POST':
        user_id = request.form['user_id']
        message = request.form['message']
        notification_service.create_notification(user_id, message)
        return redirect(url_for('notifications.list_notifications'))
    return render_template('notifications/create.html')

@bp.route('/notifications/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_notification(id):
    notification = notification_service.get_notification(id)
    if request.method == 'POST':
        message = request.form['message']
        notification_service.update_notification(id, message)
        return redirect(url_for('notifications.list_notifications'))
    return render_template('notifications/update.html', notification=notification)

@bp.route('/notifications/delete/<int:id>', methods=['POST'])
@login_required
def delete_notification(id):
    notification_service.delete_notification(id)
    return redirect(url_for('notifications.list_notifications'))
