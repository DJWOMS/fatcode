from rest_framework.permissions import BasePermissionMetaclass, BasePermission

from . import models


class IsInventoryCatUser(metaclass=BasePermissionMetaclass):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            return models.Cat.objects.filter(
                user=request.user, inventory__id=view.kwargs['id']
            ).exists()

    def has_object_permission(self, request, view, obj):
        # TODO оператор OR? Нет не слышал
        if request.user.is_superuser:
            return True
        if obj.cat.user == request.user:
            return True
        return False


class IsCatAuthUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        # TODO сразу return если сделать? Это законно?
        if obj.user == request.user:
            return True
        return False
