from celery import shared_task

from fatcode.celery import app
from src.profiles.services import send_password_to_mail


@app.task
def send_for_email(email, password):
    print('ok')
    print(email, password)
    send_password_to_mail(email, password)
