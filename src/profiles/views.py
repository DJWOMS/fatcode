from django.shortcuts import render
from rest_framework.generics import get_object_or_404
import requests

from src.profiles import models, serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, parsers
from src.profiles.services import github_get_user

def title(request):
    return render(request, 'profiles/title.html')

def done(request):
    code = request.GET.get('code')
    nik, url, email = github_get_user(code)
    try:
        account = models.Account.objects.get(nickname_git=nik)
    except models.Account.DoesNotExist:
        user = models.FatUser.objects.create(
            username=nik,
            email='test3@mail.ru',
            password='12345'
        )
        models.Account.objects.create(
            user=user,
            nickname_git=nik,
            url=url,
            email=email
        )
    return render(request, 'profiles/done.html')

class UserView(ModelViewSet):
    """Internal user display"""

    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.FatUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class UserPublicView(ModelViewSet):
    """Public user display"""

    queryset = models.FatUser.objects.all()
    serializer_class = serializers.UserPublicSerializer
    permission_classes = [permissions.AllowAny]


class SocialView(ReadOnlyModelViewSet):
    """List or one entry social display"""
    queryset = models.Social.objects.all()
    serializer_class = serializers.ListSocialSerializer

    def get_queryset(self):
        return models.Social.objects.all()


class UserAvatar(ModelViewSet):
    """Create and update user avatar"""

    parser_classes = [parsers.MultiPartParser]
    serializer_class = serializers.UserAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.FatUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj
