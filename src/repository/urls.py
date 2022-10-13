from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view()),
    path('toolkit/', views.ToolkitListView.as_view()),
    path('project/', views.ProjectsView.as_view({"get": "list"})),
    path('project/<int:pk>/', views.ProjectsView.as_view({"get": "retrieve"})),
    path('project_user/', views.UserProjectsView.as_view({"get": "list", "post": "create"})),
    path('project_user/<int:pk>/', views.UserProjectsView.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"}
    )),
]
