from rest_framework.permissions import BasePermission, IsAuthenticated

from . import models


class IsFollower(IsAuthenticated):
    """ Is Author of obj """

    def has_object_permission(self, request, view, obj):
        return obj.follower == request.user


class IsNotFollower(BasePermission):
    message = "You are already subscribed to this question."

    def has_permission(self, request, view):
        return not models.QuestionFollowers.objects.filter(
            question=request.data['question'],
            follower=request.user
        ).exists()
