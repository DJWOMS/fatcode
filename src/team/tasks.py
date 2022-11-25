from celery import shared_task

from fatcode.celery import app
from src.team.services import check_create_invitations


@app.task(bind=True)
def check_invitations():
    print("Start")
    check_create_invitations()
    print('End')
