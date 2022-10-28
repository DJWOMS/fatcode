from datetime import datetime

from src.team.models import Invitation


# def create_team_member(self, serializer):
#     """ Creating new team member and deleted this invitation"""
#     if serializer.data['accepted']:
#         TeamMember.objects.get_or_create(
#             user=self.get_object().user,
#             team=self.get_object().team
#         )
#     self.get_object().delete()


def check_create_invitations():
    """Проверка истечения даты подачи заявки"""
    month = datetime.date.today().month
    day = datetime.date.today().day
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



