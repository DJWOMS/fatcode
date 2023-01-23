from rest_framework import permissions
from rest_framework.permissions import BasePermission

from src.knowledge import models


class IsLikeNotExists(permissions.BasePermission):
    """Для создания только одной анкеты"""
    def has_permission(self, request, view):
        current_like = models.LikeDislike.objects.select_related('user').filter(user=request.user).exists()
        if not current_like:
            return True