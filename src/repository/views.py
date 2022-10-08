from rest_framework.generics import ListAPIView, UpdateAPIView
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.repository.models import Category, Toolkit, Project
from . import serializers, models, services
from .filters import ProjectFilter
from ..team.permissions import is_author_of_team_for_project


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.ProjectCategorySerializer


class ToolkitListView(ListAPIView):
    queryset = Toolkit.objects.all()
    serializer_class = serializers.ProjectToolkitSerializer


class ProjectList(ListAPIView):
    queryset = Project.objects.all()
    filterset_class = ProjectFilter
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = serializers.ProjectSerializer


class ProjectByUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Project.objects.select_related(
            'user', 'category'
        ).prefetch_related(
            'toolkit', 'teams'
        ).filter(user=request.user, teams__members__user=request.user).values()
        return Response(queryset)


class ProjectByUserPublic(APIView):
    def get(self, pk):
        queryset = Project.objects.select_related(
            'user', 'category'
        ).prefetch_related(
            'toolkit', 'teams'
        ).filter(user_id=pk, teams__members__user_id=pk).values()
        return Response(queryset)


class ProjectCreate(APIView):
    def post(self, request):
        if is_author_of_team_for_project(request.data['teams'][0], request.user):
            if models.Project.objects.filter(repository=request.data['repository']):
                return Response(status=400, data="The repository exists.")
            try:
                repository = services.get_my_repository(request.data['repository'], request.user)
            except Exception as e:
                return Response(status=400, data="The repository wasn't found.")
            project_commits = repository.get_commits()
            last_commit = repository.get_commit(project_commits[0].sha)

            teams = models.Team.objects.get(id=request.data['teams'][0])

            new_project = models.Project.objects.create(
                user=request.auth,
                name=request.data['name'],
                avatar=request.data['avatar'],
                description=request.data['description'],
                category_id=request.data['category'],
                repository=request.data['repository'],
                star_count=request.data['star'],
                fork_count=request.data['fork'],
                commit_count=request.data['commit'],
                last_commit=last_commit,
                toolkit=request.data['toolkit'][0],
                teams=teams
            )
            return Response(new_project)
        return Response(status=403, data="Forbidden")


class ProjectUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.only('name', 'description', 'repository')
    serializer_class = serializers.ProjectUpdateSerializer


class ProjectDetail(APIView):
    def get(self, pk):
        try:
            project = Project.objects.select_related(
                'user', 'category'
            ).prefetch_related(
                'teams', 'toolkit'
            ).values().get(id=pk)
        except models.Project.DoesNotExist:
            return Response(status=404, data="Does not found")
        # services.get_project_stats(project)
        return Response(project)

