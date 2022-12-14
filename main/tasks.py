from django.core.mail import mail_managers

from shop.celery import app


@app.task
def send_contact_form(email, text):
    mail_managers('Contact form', f'From: {email}\n{text}')
