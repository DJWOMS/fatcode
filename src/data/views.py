from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from src.profiles.models import FatUser
from src.profiles.serializers import DashboardUserSerializer

from src.courses.serializers import HelpUserSerializer
from src.courses.models import HelpUser

from .filters import UsersFilter, HelpUserFilter

from src.team.models import Team
from src.repository.models import Project


class UserView(ListAPIView):
    queryset = FatUser.objects.annotate(Count('courses')).all()
    permission_classes = (IsAdminUser, )
    # pagination_class = UserPaginationInfo
    # filter_backends = (DjangoFilterBackend, )
    filterset_class = UsersFilter
    serializer_class = DashboardUserSerializer


class HelpMentorView(ListAPIView):
    queryset = HelpUser.objects.all()
    permission_classes = (IsAdminUser, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = HelpUserFilter
    serializer_class = HelpUserSerializer


class TeamProjectCountView(ListAPIView):
    permission_classes = (IsAdminUser, )

    def list(self, request, *args, **kwargs):
        return Response(
            {
                'team_count': Team.objects.all().count(),
                'project_count': Project.objects.all().count()
            }
        )
