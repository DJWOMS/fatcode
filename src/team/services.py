from src.team.models import TeamMember


def create_team_member(self, serializer):
    """ Creating new team member and deleted this invitation"""
    if serializer.data['accepted']:
        TeamMember.objects.get_or_create(
            user=self.get_object().user,
            team=self.get_object().team
        )
    self.get_object().delete()
