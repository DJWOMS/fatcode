from django.urls import path

from . import views

urlpatterns = [
    path('tags/', views.TagView.as_view({'get': 'list'}), name="get-tags"),
    path('categories/', views.CategoryView.as_view({'get': 'list'}), name="get-categories"),
    path('check_work/', views.StudentWorkView.as_view(), name="check-work"),
    path('help_mentor/', views.HelpUserView.as_view(), name="help-mentor"),

    path('', views.CourseView.as_view({"get": "list", "post": "create"}), name='courses'),
    path('<int:pk>/', views.CourseView.as_view(
        {"get": "retrieve", "delete": "retrieve", "patch": "update"}
    ), name='course'),

    path('lessons/', views.LessonView.as_view({"get": "list", "post": "create"}), name='lessons'),
    path('lessons/<int:pk>/', views.LessonView.as_view(
        {"get": "retrieve", "delete": "retrieve", "patch": "update"}
    ), name='lesson')
]
