from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
import requests
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, parsers

from src.profiles import models, serializers
from src.profiles.services import (github_get_user_add,
                                   github_get_user_auth,
                                   github_auth,
                                   create_password,
                                   add_account)



def title(request):
    """Для добавления git только авторизованным"""
    if request.user.is_authenticated:
        return render(request, 'profiles/title.html')
    else:
        return render(request, 'profiles/title_auth.html')


class DoneAuthView(generics.GenericAPIView):
    """Авторизация через Гитхаб"""
    serializer_class = serializers.GitHubLoginSerializer

    def post(self, request):
        ser = serializers.GitHubLoginSerializer(data=request.data)
        if ser.is_valid():
            nik, url, email = github_get_user_auth(ser.data.get("code"))
            print(nik, url, email)
        return Response(status.HTTP_200_OK)

    def get(self, request):
        code = request.GET.get('code')
        print(code)
        nik, url, email = github_get_user_auth(code)
        print(nik, url, email)
        if email is not None:
            pass
        else:
            pass
            # return redirect('add_email')
        # try:
        #     account = models.Account.objects.get(user=request.user)
        #     return Response(status.HTTP_403_FORBIDDEN)
        # except models.Account.DoesNotExist:
        #     if email is not None:
        #         add_account(request.user, nik, url, email)
        #     else:
        #         add_account(request.user, nik, url, request.user.email)
        #         return Response(status.HTTP_200_OK)
        return Response(status.HTTP_200_OK)

#доьбавить вторую проверку на id и user
class DoneAddView(APIView):
    """Добавление git к существующему пользователю"""

    def get(self, request):
        code = request.GET.get('code')
        nik, url, email = github_get_user_add(code)
        if models.Account.objects.filter(user=request.user).exists():
            return Response('Аккаунт уже существует', status.HTTP_403_FORBIDDEN)
        if email is not None:
            add_account(request.user, nik, url, email)
        else:
            add_account(request.user, nik, url, request.user.email)
        return Response(status.HTTP_200_OK)


class AddEmail(APIView):
    '''Добавление электронной почты'''

    def post(self, request):
        serializer = serializers.CreateEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=200)
        else:
            return Response(status=400)

# def done(request):
#     """Добавление"""
#     code = request.GET.get('code')
#     print(code)
#     print(request.user)
#     nik, url, email = github_get_user(code)
#     if request.user.is_authenticated:
#         print('auth')
#         try:
#             account = models.Account.objects.get(email=email, user=request.user)
#             print('ok')
#         except models.Account.DoesNotExist:
#             models.Account.objects.create(
#                 user=request.user,
#                 nickname_git=nik,
#                 url=url,
#                 email=email
#             )
#             print('create')
#         return render(request, 'profiles/done.html')
#     # else:
#     #     print('no auth')
#     #     try:
#     #         user = models.FatUser.objects.get(email=email)
#     #         account = models.Account.objects.get(email=email)
#     #         user_id, token = github_auth(user.id)
#     #         return render(request, 'profiles/done.html')
#     #     except models.Account.DoesNotExist:
#     #         print('no ex')
#     #         user = models.FatUser.objects.create(
#     #             username=nik,
#     #             email=email,
#     #             password=create_password()
#     #         )
#     #         user_id, token = github_auth(user.id)
#     return render(request, 'profiles/done.html')




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
