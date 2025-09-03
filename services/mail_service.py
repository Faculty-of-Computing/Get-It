from flask import url_for
from flask_mail import Message
from core.database import db
from core.configs import SMTP_SEND_FROM

def send_password_reset_email(user):
    from flask import current_app
    token = user.get_reset_token()
    mail = getattr(current_app, 'mail', None)
    msg = Message('Password Reset Request',
                  sender=SMTP_SEND_FROM,
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    if mail:
        mail.send(msg)
