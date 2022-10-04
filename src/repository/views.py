from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from src.repository.models import Category, Toolkit, Project
from . import serializers
from .filters import ProjectFilter


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryListSerializer


class ToolkitListView(ListAPIView):
    queryset = Toolkit.objects.all()
    serializer_class = serializers.ToolkitListSerializer


class ProjectList(ListAPIView):
    queryset = Project.objects.all()
    filterset_class = ProjectFilter
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = serializers.ProjectListSerializer


# def project_list(request, filters: schemas.Filters = Query(...)):
#     projects = models.Project.objects.all()
#     # services.get_projects_stats(projects)
#     _filters = filters.dict(exclude_none=True)
#
#     _date_min = date.today() - timedelta(days=_filters.pop('last_commit_min'))
#     _date_max = date.today() - timedelta(days=_filters.pop('last_commit_max'))
#
#     projects = projects.filter(
#         star_count__range=(_filters.pop('star_min'), _filters.pop('star_max')),
#         fork_count__range=(_filters.pop('fork_min'), _filters.pop('fork_max')),
#         commit_count__range=(_filters.pop('commit_min'), _filters.pop('commit_max')),
#         last_commit__date__range=(_date_max, _date_min),
#         # **_filters
#     )
#     if _filters.get('name'):
#         projects = projects.filter(name__icontains=_filters.get('name'))
#     if _filters.get('category_id'):
#         projects = projects.filter(category__id=_filters.get('category_id'))
#     if _filters.get('toolkit'):
#         projects = projects.filter(toolkit__id=_filters.get('toolkit'))
#     return projects
#
#
# def project_by_user(request):
#     return models.Project.objects.select_related(
#         'user', 'category', 'team'
#     ).prefetch_related(
#         'toolkit'
#     ).filter(Q(user=request.auth) | Q(team__members__user=request.auth)).distinct()
#
#
# # @repository.get("project/by_user/{user_id}/", response=List[schemas.Project], auth=AuthToken())
# # def project_by_user_public(request, user_id: int):
# #     return models.Project.objects.select_related(
# #         'user', 'category', 'team'
# #     ).prefetch_related('toolkit').filter(Q(user_id=user_id) | Q(team__members__user_id=user_id))
#
#
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
