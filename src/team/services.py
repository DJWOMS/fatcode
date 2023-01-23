from datetime import date

from ..base import exceptions

from src.team import models


def check_create_invitations():
    """Проверка истечения даты подачи заявки"""
    month = date.today().month
    day = date.today().day
    invitations = models.Invitation.objects.all()
    for invitation in invitations:
        create_month = invitation.create_date.date().month
        create_day = invitation.create_date.date().day
        if month > create_month and day > create_day:
            invitation.delete()
        elif month > (create_month + 1):
            invitation.delete()
        else:
            pass


def check_and_create_invitation(team, cur_user):
    """Проверка и создание заявки"""
    user = models.Team.objects.filter(user=cur_user.id, id=team.id).exists()
    member = models.TeamMember.objects.filter(user=cur_user, team=team).exists()
    invitation = models.Invitation.objects.filter(team=team, user=cur_user, order_status='Waiting').exists()
    if user or member or invitation:
        raise exceptions.CustomException()
    else:
        invitation = models.Invitation.objects.create(team=team, user=cur_user)
        return invitation


def check_and_create_team_member(instance):
    """Проверка и создание участника команды"""
    current_member = models.TeamMember.objects.filter(user=instance.user, team=instance.team).exists()
    if current_member:
        raise exceptions.TeamMemberException()
    if instance.order_status == 'Approved':
        return models.TeamMember.objects.create(user=instance.user, team=instance.team)


def check_post(post_id, **validated_data):
    """Проверка поста"""
    parent = validated_data.get('parent')
    if parent is not None:
        try:
            post = models.Post.objects.get(id=validated_data.get('parent').post.id)
        except models.Post.DoesNotExist:
            raise exceptions.PostNotExistsException()
        if post.id != post_id:
            raise exceptions.PostException()
        return parent


def check_teams(teams, user):
    """Проверка является ли пользователь участником команды"""
    if teams is not None:
        for team in teams:
            if not models.TeamMember.objects.filter(user=user, team=team).exists():
                raise exceptions.TeamMemberExists()
    return teams


def check_my_teams(teams, user):
    """Проверка автора команд"""
    for team in teams:
        team = models.Team.objects.filter(user=user, id=team.id).exists()
        if not team:
            raise exceptions.TeamAuthor()
    return teams






