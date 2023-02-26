from django.urls import path

from src.questionnaire import views


urlpatterns = [
    path('', views.QuestionnaireView.as_view({"get": "list", "post": "create"}), name='questionnaire'),
    path('<int:pk>/', views.QuestionnaireView.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"}
        ), name='questionnaire_detail'),
    path('<int:pk>/teams/', views.QuestionnaireTeamsView.as_view(
            {"get": "list", "put": "update"}
        ), name='questionnaire_detail_teams'),
    path('<int:pk>/projects/', views.QuestionnaireProjectsView.as_view(
            {"get": "list", "put": "update"}
        ), name='questionnaire_detail_projects'),
    path('<int:pk>/accounts/', views.QuestionnaireAccountsView.as_view(
            {"get": "list", "put": "update"}
        ), name='questionnaire_detail_accounts'),
    path('<int:pk>/avatar/', views.AvatarQuestionnaireView.as_view(
        {"get": "list", "put": "update"}
        ), name='questionnaire_avatar')
]