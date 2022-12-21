from django.db.models import Q
from django.shortcuts import render
from django_filters import rest_framework as filter

from rest_framework import generics, status, parsers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from src.profiles import models, serializers, services, filters, permissions
from src.base.permissions import IsUser
from src.base.classes import MixedPermissionSerializer, MixedSerializer, MixedPermission


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
            if internal_token := services.check_account_for_auth(account_id):
                serializer = serializers.TokenSerializer(internal_token)
                return Response(serializer.data)
            else:
                internal_token = services.create_user_and_token(account_id, email, account_name, account_url)
                serializer = serializers.TokenSerializer(internal_token)
                return Response(serializer.data)


class AddGitHub(generics.GenericAPIView):
    """Добавление git к существующему пользователю"""
    serializer_class = serializers.GitHubAddSerializer

    def post(self, request):
        ser = serializers.GitHubAddSerializer(data=request.data)
        if ser.is_valid():
            account_name, account_url, account_id = services.github_get_user_add(ser.data.get("code"))
            if services.check_account_for_add(request.user, account_id):
                services.create_account(request.user, account_name, account_url, account_id)
                return Response(status.HTTP_200_OK)


class LanguageListView(generics.ListAPIView):
    """Представление языков"""
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguagesSerializer


class SocialView(generics.ListAPIView):
    """Представление ссоциальных сетей"""
    queryset = models.Social.objects.all()
    serializer_class = serializers.SocialListSerializer


class UsersView(MixedPermissionSerializer, ModelViewSet):
    """Представление пользователя"""

    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,)
    }
    serializer_classes_by_action = {
        'list': serializers.UserProfileListSerializer,
        'retrieve': serializers.UserProfileSerializer
    }

    def get_queryset(self):
        return models.FatUser.objects.all().prefetch_related('user_social')


class AdditionallyProfileView(MixedSerializer, ModelViewSet):
    """Представление дополнительных данных профиля"""

    serializer_classes_by_action = serializers.AdditionallyProfileSerializer
    permission_classes_by_action = (IsAuthenticated,)

    def get_queryset(self):
        return models.Questionnaire.objects.select_related('user').filter(user_id=self.kwargs.get('pk'))


class UserMeView(MixedPermissionSerializer, ModelViewSet):
    """Представление пользователя только для владельца аккаунта"""
    permission_classes_by_action = {
        'list': (IsAuthenticated, permissions.IsMeAuthor,),
        'update': (IsAuthenticated, permissions.IsMeAuthor,),
        'destroy': (IsAuthenticated, permissions.IsMeAuthor,),
    }
    serializer_classes_by_action = {
        'list': serializers.UserMeProfileSerializer,
        'update': serializers.UserProfileUpdateSerializer,
        'destroy': serializers.UserProfileSerializer
    }

    def get_queryset(self):
        return models.FatUser.objects.filter(username=self.request.user)

    def get_object(self):
        return models.FatUser.objects.get(username=self.request.user)

    def perform_update(self, serializer):
        serializer.save(pk=self.request.user.id)


class AvatarProfileView(MixedPermissionSerializer, ModelViewSet):
    """Аватар профиля"""
    parser_classes = (parsers.MultiPartParser,)
    serializer_classes_by_action = serializers.AvatarProfileSerializer
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly,),
        'update': (IsAuthenticated, permissions.IsMeAuthor,)
    }

    def get_queryset(self):
        return models.FatUser.objects.select_related('questionnaire').filter(username=self.request.user)

    def get_object(self):
        return models.FatUser.objects.select_related('questionnaire').get(username=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)


class SocialProfileView(MixedSerializer, ModelViewSet):
    """Социальные ссылки профиля"""
    serializer_classes_by_action = {
        'list': serializers.SocialProfileSerializer,
        'retrieve': serializers.SocialProfileSerializer,
        'create': serializers.SocialProfileCreateSerializer,
        'update': serializers.SocialProfileUpdateSerializer,
        'destroy': serializers.SocialProfileCreateSerializer
    }
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'create': (IsAuthenticated, permissions.IsMeAuthor, ),
        'update': (IsAuthenticated, permissions.IsMeAuthor,),
        'destroy': (IsAuthenticated, permissions.IsMeAuthor,),
    }
    lookup_url_kwarg = 'social_pk'

    def get_queryset(self):
        return models.FatUserSocial.objects.filter(user=self.request.user).select_related('user', 'social')


class QuestionnaireView(MixedPermissionSerializer, ModelViewSet):
    """CRUD анкеты пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'create': (IsAuthenticated, permissions.IsQuestionnaireNotExists,),
        'retrieve': (IsAuthenticated, ),
        'update': (IsAuthenticated, IsUser,),
        'destroy': (IsAuthenticated, IsUser,),
    }
    serializer_classes_by_action = {
        'list': serializers.QuestionnaireListSerializer,
        'retrieve': serializers.QuestionnaireDetailSerializer,
        'create': serializers.CUDQuestionnaireSerializer,
        'update': serializers.UDQuestionnaireSerializer,
        'destroy': serializers.CUDQuestionnaireSerializer
    }
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_class = filters.ToolkitFilter

    def get_queryset(self):
        return models.Questionnaire.objects.all().select_related('user').prefetch_related(
            'toolkits',
            'languages',
            'socials'
        )

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class QuestionnaireTeamsView(MixedPermissionSerializer, ModelViewSet):
    """RD  команд в анкете пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUser,)
    }
    serializer_classes_by_action = {
        'list': serializers.TeamsListQuestionnaireSerializer,
        'update': serializers.UTeamsQuestionnaireSerializer
    }

    def get_queryset(self):
        return models.Questionnaire.objects.all().select_related('user').prefetch_related('teams')

    def perform_update(self, serializer):
        serializer.save()


class QuestionnaireProjectsView(MixedPermissionSerializer, ModelViewSet):
    """RU репозиториев в анкете пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUser,)
    }
    serializer_classes_by_action = {
        'list': serializers.ProjectsListQuestionnaireSerializer,
        'update': serializers.UProjectsQuestionnaireSerializer
    }

    def get_queryset(self):
        return models.Questionnaire.objects.all().select_related('user').prefetch_related('projects')

    def perform_update(self, serializer):
        serializer.save()


class QuestionnaireAccountsView(MixedPermissionSerializer, ModelViewSet):
    """RU аккаунтов в анкете пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUser,)
    }
    serializer_classes_by_action = {
        'list': serializers.AccountsListQuestionnaireSerializer,
        'update': serializers.UAccountsQuestionnaireSerializer
    }

    def get_queryset(self):
        return models.Questionnaire.objects.all().select_related('user').prefetch_related('accounts')

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class AvatarQuestionnaireView(MixedPermissionSerializer, ModelViewSet):
    """Аватар анкеты"""
    parser_classes = (parsers.MultiPartParser,)
    serializer_classes_by_action = serializers.AvatarQuestionnaireSerializer
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'update': (IsAuthenticated, permissions.IsAuthorQuestionnaireUser,)
    }

    def get_queryset(self):
        return models.Questionnaire.objects.filter(id=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        serializer.save(questionnaire_id=self.kwargs.get('pk'))


class ApplicationView(MixedSerializer, ModelViewSet):
    """CRD заявки"""
    serializer_classes_by_action = {
        'list': serializers.ApplicationListSerializer,
        'create': serializers.ApplicationSerializer,
        'delete': serializers.ApplicationSerializer
    }
    permission_classes = (IsAuthenticated, )
    permission_classes_by_action = {
        'create': (permissions.IsNotApplicant, permissions.IsNotYouGetter, permissions.IsNotAlreadyFriend, ),
    }

    def get_queryset(self):
        return models.Applications.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ApplicationUserGetterView(ReadOnlyModelViewSet):
    """Представление заявки пользователя"""
    serializer_class = serializers.ApplicationListSerializer
    permissions = (IsAuthenticated, )

    def get_queryset(self):
        return models.Applications.objects.filter(getter=self.request.user)


class FriendView(MixedSerializer, ModelViewSet):
    """Друзья пользователя"""
    serializer_classes_by_action = {
        'list': serializers.FriendListSerializer,
        'create': serializers.FriendSerializer,
        'delete': serializers.FriendListSerializer
    }
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return models.Friends.objects.filter(Q(user=self.request.user) | Q(friend=self.request.user))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# class UserPublicView(ModelViewSet):
#     """Public user display"""
#
#     queryset = models.FatUser.objects.all()
#     serializer_class = serializers.UserPublicSerializer
#     permission_classes = (AllowAny, )
# class SocialView(ReadOnlyModelViewSet):
#     """List or one entry social display"""
#     queryset = models.Social.objects.all()
#     serializer_class = serializers.ListSocialSerializer
#
#     def get_queryset(self):
#         return models.Social.objects.all()
#
#
# class UserAvatar(ModelViewSet):
#     """Create and update user avatar"""
#
#     parser_classes = (parsers.MultiPartParser, )
#     serializer_class = serializers.UserAvatarSerializer
#     permission_classes = (IsAuthenticated, )
#
#     def get_queryset(self):
#         return models.FatUser.objects.filter(id=self.request.user.id)
#
#     def get_object(self):
#         queryset = self.filter_queryset(self.get_queryset())
#         obj = get_object_or_404(queryset)
#         self.check_object_permissions(self.request, obj)
#         return obj

# class UsersView(ReadOnlyModelViewSet):
#     queryset = models.FatUser.objects.all()
#     serializer_class = serializers.GetUserSerializer
#     permission_classes = (IsAuthenticated, )
