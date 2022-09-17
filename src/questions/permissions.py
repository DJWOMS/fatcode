from rest_framework.permissions import BasePermissionMetaclass


class IsAuthor(metaclass=BasePermissionMetaclass):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view,  obj):
        if request.user.is_superuser:
            return True

        if obj.author == request.user:
            return True

        return False


