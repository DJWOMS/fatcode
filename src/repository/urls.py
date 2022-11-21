from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('toolkit/', views.ToolkitListView.as_view(), name='toolkit'),
    path('project/', views.ProjectsView.as_view({"get": "list", "post": "create"}), name='project'),
    path('project/<int:pk>/', views.ProjectsView.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"}), name='project_detail'),
    path('project/<int:pk>/teams/', views.MemberProjectTeamsView.as_view({"get": "list"}), name='project_teams'),
    path('project/<int:pk>/board/', views.MemberProjectBoardView.as_view({"get": "list"}), name='project_board'),
    path('my_projects/', views.UserProjectsView.as_view({"get": "list"}), name='my_projects'),
]
