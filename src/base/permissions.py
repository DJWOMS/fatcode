from rest_framework.permissions import IsAuthenticated


class IsAuthor(IsAuthenticated):
    """ Is Author of obj """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsUser(IsAuthenticated):
    """ Is Author of obj """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user