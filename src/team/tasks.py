from fatcode.celery import app
from src.team.services import check_create_invitations


@app.task
def check_invitations():
    check_create_invitations()
