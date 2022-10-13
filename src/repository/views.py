from rest_framework import generics, viewsets, permissions
from django_filters import rest_framework as filters

from .filters import ProjectFilter
from ..base.classes import MixedSerializer, MixedPermissionSerializer

from . import serializers, models
from ..base.permissions import IsAuthor


class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ToolkitListView(generics.ListAPIView):
    queryset = models.Toolkit.objects.all()
    serializer_class = serializers.ToolkitSerializer


class ProjectsView(MixedSerializer, viewsets.ReadOnlyModelViewSet):
    queryset = (
        models.Project.objects
        .select_related('user', 'category')
        .prefetch_related('toolkit', 'teams')
        .all()
    )
    filterset_class = ProjectFilter
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_classes_by_action = {
        'list': serializers.ProjectListSerializer,
        'retrieve': serializers.ProjectDetailSerializer
    }


class UserProjectsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    permission_classes = (IsAuthor,)
    # TODO добавить проверку при создании, что команды это команды пользователя
    # TODO добавить проверку репозитория
    permission_classes_by_action = {'create': (permissions.IsAuthenticated,)}
    serializer_classes_by_action = {
        'create': serializers.ProjectSerializer,
        'list': serializers.ProjectListSerializer,
        'retrieve': serializers.ProjectDetailSerializer,
        'update': serializers.ProjectSerializer,
        'destroy': serializers.ProjectSerializer
    }

    def get_queryset(self):
        return (
            models.Project.objects
            .select_related('user', 'category')
            .prefetch_related('toolkit', 'teams')
            .filter(user=self.request.user, teams__members__user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class ProjectByUserPublic(APIView):
#     def get(self, request, pk):
#         queryset = models.Project.objects.select_related(
#             'user', 'category'
#         ).prefetch_related(
#             'toolkit', 'teams'
#         ).filter(user_id=pk, teams__members__user_id=pk).values()
#         return Response(queryset)


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
#
# @repository.put("project/{project_id}/", response=schemas.Project, auth=AuthToken())
# def project_update(request, project_id: int, project: schemas.ProjectUpdate):
#     _data_project = get_object_or_404(models.Project, id=project_id, user=request.auth)
#     _tool_kit = project.dict().pop('toolkit')
#     for attr, value in project.dict(exclude={'toolkit'}).items():
#         setattr(_data_project, attr, value)
#     _data_project.save()
#     _data_project.toolkit.set(_tool_kit)
#     return _data_project
#
#
# # @repository.put("project/avatar/{project_id}/", response=schemas.Project) #, auth=AuthToken())
# # def project_update_avatar(request, project_id: int, avatar: UploadedFile = Form(...)):
# #     _data_project = get_object_or_404(models.Project, id=project_id, user=request.auth)
# #     print(avatar)
# #     return _data_project
#
# def project_detail(request, project_id: int):
#     try:
#         project = models.Project.objects.select_related(
#             'user', 'category', 'team'
#         ).prefetch_related('toolkit').get(id=project_id)
#     except models.Project.DoesNotExist:
#         return Response(status=404, data="Does not found")
#     services.get_project_stats(project)
#     return project
