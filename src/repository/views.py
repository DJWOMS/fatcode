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
    def get(self, request, pk):
        queryset = Project.objects.select_related(
            'user', 'category'
        ).prefetch_related(
            'toolkit', 'teams'
        ).filter(user_id=pk, teams__members__user_id=pk).values()
        return Response(queryset)


class ProjectCreate(APIView):
    def post(self, request):
        if is_author_of_team_for_project(1, request.auth):
            print("ok")
        else:
            print("no")


# def project_create(request, project: schemas.ProjectCreate):
#     if is_author_of_team_for_project(project.team_id, request.auth):
#         if models.Project.objects.filter(repository=project.repository):
#             return Response(status=400, data="The repository exists.")
#         try:
#             repository = services.get_my_repository(project.repository, request.auth)
#         except Exception as e:
#             return Response(status=400, data="The repository wasn't found.")
#         project_commits = repository.get_commits()
#         last_commit = repository.get_commit(project_commits[0].sha)
#
#         team = models.Team.objects.get(id=project.team_id)
#
#         new_project = models.Project.objects.create(
#             user=request.auth,
#             name=project.name,
#             avatar=team.avatar,
#             description=project.description,
#             category_id=project.category_id,
#             repository=repository.html_url,
#             star_count=repository.stargazers_count,
#             fork_count=repository.forks_count,
#             commit_count=project_commits.totalCount,
#             last_commit=last_commit.commit.committer.date,
#             team=team
#         )
#         new_project.toolkit.add(*project.toolkit)
#
#         return new_project
#     return Response(status=403, data="Forbidden")
#


class ProjectUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.only('name', 'description', 'repository')
    serializer_class = serializers.ProjectUpdateSerializer


# # @repository.put("project/avatar/{project_id}/", response=schemas.Project) #, auth=AuthToken())
# # def project_update_avatar(request, project_id: int, avatar: UploadedFile = Form(...)):
# #     _data_project = get_object_or_404(models.Project, id=project_id, user=request.auth)
# #     print(avatar)
# #     return _data_project


class ProjectDetail(APIView):
    def get(self, request, pk):
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

