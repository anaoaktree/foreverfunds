from services.login_service import password_generator
from flask_mail import Message
from flask import render_template
from db.user_helper import add_user


def send_email(new_user_name, new_user_email, is_admin, mail_service):
    password = password_generator()
    add_user(new_user_name, password, is_admin)
    msg = Message('New account at foreverfunds', recipients=[new_user_email])
    msg.body = render_template('emails/account_creation.html', username=new_user_name, password=password)
    msg.html = render_template('emails/account_creation.html', username=new_user_name, password=password)
    # mail_service.send(msg) ## TODO: uncomment this in production to send email
    return "New user sucessfully created!"
