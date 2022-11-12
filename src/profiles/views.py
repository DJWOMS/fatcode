from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, parsers

from src.profiles import models, serializers, services
from src.base.permissions import IsUser


def title(request):
    """Для добавления git только авторизованным"""
    if request.user.is_authenticated:
        return render(request, 'profiles/title.html')
    else:
        return render(request, 'profiles/title_auth.html')


class GitGubAuthView(generics.GenericAPIView):
    """Авторизация через Гитхаб"""
    serializer_class = serializers.GitHubAddSerializer

    def post(self, request):
        ser = serializers.GitHubAddSerializer(data=request.data)
        if ser.is_valid():
            account_name, account_url, account_id, email = services.github_get_user_auth(ser.data.get("code"))
            print(email)
            try:
                account = models.Account.objects.get(account_id=account_id)
                user_id, internal_token = services.github_auth(account.user.id)
                return Response(status.HTTP_200_OK)
            except models.Account.DoesNotExist:
                if email is not None:
                    user = services.create_user_with_email(account_id, email)
                    if user:
                        password = services.create_password()
                        user.set_password(password)
                        user.save()
                        services.create_account(user, account_name, account_url, account_id)
                        user_id, internal_token = services.github_auth(user.id)
                        return Response(status.HTTP_200_OK)
                    else:

                elif email is None:
                    user = services.create_user(account_id)
                    password = services.create_password()
                    user.set_password(password)
                    user.save()
                    services.create_account(user, account_name, account_url, account_id)
                    user_id, internal_token = services.github_auth(user.id)
                    return Response(status.HTTP_200_OK)


class AddGitHub(generics.GenericAPIView):
    """Добавление git к существующему пользователю"""
    serializer_class = serializers.GitHubAddSerializer

    def post(self, request):
        ser = serializers.GitHubAddSerializer(data=request.data)
        if ser.is_valid():
            account_name, account_url, account_id = services.github_get_user_add(ser.data.get("code"))
            if models.Account.objects.filter(user=request.user, account_id=account_id).exists():
                return Response('Аккаунт уже существует', status.HTTP_403_FORBIDDEN)
            if models.Account.objects.filter(account_id=account_id).exists():
                return Response('Аккаунт уже привязан', status.HTTP_403_FORBIDDEN)
            services.create_account(request.user, account_name, account_url, account_id)
        return Response(status.HTTP_200_OK)


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
