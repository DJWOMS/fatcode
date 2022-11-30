from django.urls import path
from . import views

urlpatterns = [
    path("answer/", views.AnswerView.as_view({"post": "create"}), name="create-answer"),
    path("answer/<int:pk>/", views.AnswerView.as_view(
        {"patch": "update", "delete": "destroy"}), name="answer"
    ),
    path("review/", views.CreateQuestionReview.as_view({"post": "create"}), name="question-review"),
    path("answer_review/", views.CreateAnswerReview.as_view(
        {"post": "create"}), name="answer-review"
    ),

    path("follow/", views.QuestionFollower.as_view({"post": "create", "get": "list"})),
    path("follow/<int:pk>/", views.QuestionFollower.as_view({"delete": "destroy"})),

    path("answer/<int:pk>/accept", views.UpdateAnswerAccept.as_view({"patch": "update"})),
    path("<int:pk>/", views.QuestionView.as_view(
        {"get": "retrieve", "patch": "update", "delete": "destroy"}), name="question"
    ),
    path("", views.QuestionView.as_view({"get": "list", "post": "create"}), name="questions"),
]
