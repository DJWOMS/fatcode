
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from src.profiles import models


class IsNotApplicant(BasePermission):
    message = "You already have application to this user."

    def has_permission(self, request, view):
        return not models.Applications.objects.filter(getter=request.data['getter'], sender=request.user).exists()


class IsNotAlreadyFriend(BasePermission):
    message = "You have already friends with this user."

    def has_permission(self, request, view):
        return not models.Friends.objects.filter(friend=request.data['getter'], user=request.user).exists()


class IsNotYouGetter(BasePermission):
    message = "You can't send a friend request to yourself."

    def has_permission(self, request, view):
        return request.data['getter'] == request.user.id


class IsQuestionnaireNotExists(permissions.BasePermission):
    """Для создания только одной анкеты"""

    def has_permission(self, request, view):
        cur_user = models.Questionnaire.objects.select_related('user').filter(user=request.user).exists()
        if not cur_user:
            return True


class IsAuthorUser(BasePermission):
    """Только для автора пользователя"""
    def has_permission(self, request, view):
        return models.FatUser.objects.filter(username=request.user, id=view.kwargs.get('pk')).exists()


class IsAuthorQuestionnaireUser(BasePermission):
    """Только для автора пользователя"""
    def has_permission(self, request, view):
        return models.Questionnaire.objects.select_related('user').filter(
            user=request.user, id=view.kwargs.get('pk')
        ).exists()


class IsMeAuthor(BasePermission):
    """Только для автора профиля"""
    def has_permission(self, request, view):
        return models.FatUser.objects.filter(username=request.user).exists()