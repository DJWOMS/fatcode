from celery import shared_task

from fatcode.celery import app
from src.team.services import check_create_invitations


@app.task
def check_invintations():
    check_create_invitations()