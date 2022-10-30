from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from src.profiles.models import FatUser
from django_filters.rest_framework import DjangoFilterBackend
from src.profiles.serializers import DashboardUserSerializer
from src.courses.serializers import HelpUserSerializer
from .filters import UsersFilter, HelpUserFilter
from src.courses.models import HelpUser
from src.team.models import Team
from src.repository.models import Project
from django.db.models import Sum, Count, Q
from rest_framework.pagination import LimitOffsetPagination


class UserPaginationInfo(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        info = FatUser.objects.all().aggregate(
            Sum('coins'),
            Sum('experience'),
            started_courses_count=Count('courses', filter=Q(courses__progress=0)),
            finished_courses_count=Count('courses', filter=Q(courses__progress=100))
        )
        return Response({'user_info': info, 'results': data})


class UserView(ListAPIView):
    queryset = FatUser.objects.annotate(Count('courses')).all()
    permission_classes = [IsAdminUser]
    pagination_class = UserPaginationInfo
    filter_backends = (DjangoFilterBackend, )
    filterset_class = UsersFilter
    serializer_class = DashboardUserSerializer


class HelpMentorView(ListAPIView):
    queryset = HelpUser.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = HelpUserFilter
    serializer_class = HelpUserSerializer


class TeamProjectCountView(ListAPIView):
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        return Response(
            {
                'team_count': Team.objects.all().count(),
                'project_count': Project.objects.all().count()
            }
        )
