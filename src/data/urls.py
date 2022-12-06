from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UserView.as_view()),
    path('help_mentor/', views.HelpMentorView.as_view()),
    path('team_project_count/', views.TeamProjectCountView.as_view())
]
