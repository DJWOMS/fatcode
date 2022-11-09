from rest_framework.permissions import BasePermission

from . import models


class IsNotFollower(BasePermission):
    def has_permission(self, request, view):
        if models.QuestionFollowers.objects.filter(question=request.data['question'], follower=request.user):
            return False
        return True
