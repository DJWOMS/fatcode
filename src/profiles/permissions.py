from rest_framework.permissions import BasePermission

from src.profiles import models


class IsNotApplicant(BasePermission):
    message = "You already have application to this user."

    def has_permission(self, request, view):
        if models.Applications.objects.filter(getter=request.data['getter'], sender=request.user):
            return False
        return True


class IsNotAlreadyFriend(BasePermission):
    message = "You have already friends with this user."

    def has_permission(self, request, view):
        if models.Friends.objects.filter(friend=request.data['getter'], user=request.user):
            return False
        return True


class IsNotYouGetter(BasePermission):
    message = "You can't send a friend request to yourself."

    def has_permission(self, request, view):
        if request.data['getter'] == request.user.id:
            return False
        return True