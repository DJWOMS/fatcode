from rest_framework.permissions import BasePermissionMetaclass
from . import models


class IsInventoryCatUser(metaclass=BasePermissionMetaclass):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            cat_user = models.Cat.objects.filter(user=request.user, inventory__id=view.kwargs['id']).exists()
            return cat_user

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.cat.user == request.user:
            return True
        return False
