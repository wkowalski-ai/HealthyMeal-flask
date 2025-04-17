from flask_mail import Message
from flask import current_app, url_for
from . import mail

def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients, body=body)
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    subject = "Resetowanie hasła w HealthyMeal"
    text_body = f"""
Cześć!

Aby zresetować swoje hasło, kliknij poniższy link:
{reset_url}

Jeśli to nie Ty prosiłeś o reset hasła, po prostu zignoruj tę wiadomość.

Pozdrawiamy,
Zespół HealthyMeal
"""
    html_body = f"""
    <p>Cześć!</p>
    <p>Aby zresetować swoje hasło, kliknij poniższy link:</p>
    <p><a href="{reset_url}">{reset_url}</a></p>
    <p>Jeśli to nie Ty prosiłeś o reset hasła, po prostu zignoruj tę wiadomość.</p>
    <p>Pozdrawiamy,<br>Zespół HealthyMeal</p>
    """
    msg = Message(subject=subject,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email],
                  body=text_body,
                  html=html_body)
    mail.send(msg)
