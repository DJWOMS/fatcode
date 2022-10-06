from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name="category-list"),
    path('toolkit/', views.ToolkitListView.as_view(), name="toolkit-list"),
    path('project/', views.ProjectList.as_view(), name="project-list"),
    path('project_by_user/', views.ProjectByUser.as_view(), name="project-by-user"),
    path('project_by_user/<int:pk>', views.ProjectByUserPublic.as_view(), name="project-by-user-public"),
]
