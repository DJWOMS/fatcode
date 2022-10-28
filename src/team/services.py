from datetime import datetime, date

from src.team.models import Invitation


def check_create_invitations():
    """Проверка истечения даты подачи заявки"""
    month = date.today().month
    day = date.today().day
    invitations = Invitation.objects.all()
    for invitation in invitations:
        create_month = invitation.create_date.date().month
        create_day = invitation.create_date.date().day
        if month > create_month and day > create_day:
            invitation.delete()
        elif month > (create_month + 1):
            invitation.delete()
        else:
            pass



