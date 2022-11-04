from django.urls import path
from . import views

urlpatterns = [
    path("answer/", views.AnswerView.as_view({"post": "create"})),
    path("answer/<int:pk>/", views.AnswerView.as_view({"put": "update", "delete": "destroy"})),
    path("review/", views.CreateQuestionReview.as_view({"post": "create"})),
    path("answer_review/", views.CreateAnswerReview.as_view({"post": "create"})),
    path("<int:pk>/", views.QuestionView.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"}
    )),
    path("answer/<int:pk>/accept", views.UpdateAnswerAccept.as_view({"patch": "update"})),
    path("", views.QuestionView.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/follow/", views.QuestionFollower.as_view({"post": "create", "delete": "destroy"}))
]
