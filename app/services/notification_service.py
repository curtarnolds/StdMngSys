from app.models import Notification
from app import db

def create_notification(user_id, message):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()
    return notification

def get_notification(notification_id):
    return Notification.query.get(notification_id)

def update_notification(notification_id, message):
    notification = Notification.query.get(notification_id)
    notification.message = message
    db.session.commit()
    return notification

def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    db.session.delete(notification)
    db.session.commit()
