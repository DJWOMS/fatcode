from django_filters import rest_framework as filter

from rest_framework import parsers, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from src.questionnaire import models, serializers, services, filters, permissions
from src.base.permissions import IsUser
from src.base.classes import MixedPermissionSerializer, MixedSerializer, MixedPermission


class QuestionnaireView(MixedPermissionSerializer, ModelViewSet):
    """CRUD анкеты пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'create': (IsAuthenticated, permissions.IsQuestionnaireNotExists),
        'retrieve': (IsAuthenticated, ),
        'update': (IsAuthenticated, IsUser),
        'destroy': (IsAuthenticated, IsUser),
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
        return models.Questionnaire.objects.select_related('user').prefetch_related(
            'toolkits',
            'languages',
            'socials'
        ).all()

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
        'update': (IsAuthenticated, IsUser)
    }
    serializer_classes_by_action = {
        'list': serializers.TeamsListQuestionnaireSerializer,
        'update': serializers.UTeamsQuestionnaireSerializer
    }

    def get_queryset(self):
        return models.Questionnaire.objects.select_related('user').prefetch_related('teams').all()

    def perform_update(self, serializer):
        serializer.save()


class QuestionnaireProjectsView(MixedPermissionSerializer, ModelViewSet):
    """RU репозиториев в анкете пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUser)
    }
    serializer_classes_by_action = {
        'list': serializers.ProjectsListQuestionnaireSerializer,
        'update': serializers.UProjectsQuestionnaireSerializer
    }

    def get_queryset(self):
        return models.Questionnaire.objects.select_related('user').prefetch_related('projects').all()

    def perform_update(self, serializer):
        serializer.save()


class QuestionnaireAccountsView(MixedPermissionSerializer, ModelViewSet):
    """RU аккаунтов в анкете пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'update': (IsAuthenticated, IsUser)
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
        'update': (IsAuthenticated, permissions.IsAuthorQuestionnaireUser)
    }

    def get_queryset(self):
        return models.Questionnaire.objects.filter(id=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        serializer.save(questionnaire_id=self.kwargs.get('pk'))

