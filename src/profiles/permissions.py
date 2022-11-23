from rest_framework import permissions
from .models import Questionnaire

class IsQuestionnaireNotExists(permissions.BasePermission):
    """Для создания только одной анкеты"""

    def has_permission(self, request, view):
        cur_user = Questionnaire.objects.filter(user=request.user).exists()
        if not cur_user:
            return True