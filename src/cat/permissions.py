from rest_framework.permissions import BasePermissionMetaclass


class IsUserCat(metaclass=BasePermissionMetaclass):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view,  obj):
        if request.user.is_superuser:
            return True

        if obj.user == request.user:
            return True

        return False

