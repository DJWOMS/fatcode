from rest_framework.permissions import IsAuthenticated


class IsUser(IsAuthenticated):
    """ Is Author of obj where only user """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthor(IsAuthenticated):
    """ Is Author of obj """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
