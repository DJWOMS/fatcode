from rest_framework import permissions
from rest_framework.permissions import BasePermission

from src.questionnaire import models


class IsQuestionnaireNotExists(permissions.BasePermission):
    """Для создания только одной анкеты"""
    def has_permission(self, request, view):
        current_user = models.Questionnaire.objects.select_related('user').filter(user=request.user).exists()
        if not current_user:
            return True


class IsAuthorQuestionnaireUser(BasePermission):
    """Только для автора пользователя"""
    def has_permission(self, request, view):
        return models.Questionnaire.objects.select_related('user').filter(
            user=request.user, id=view.kwargs.get('pk')
        ).exists()
