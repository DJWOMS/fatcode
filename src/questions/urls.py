from django.urls import path
from . import views

urlpatterns = [
    path("answer/", views.AnswerView.as_view({"post": "create"})),
    path("answer/<int:id>/", views.AnswerView.as_view({"put": "update", "delete": "destroy"})),
    path("review/", views.CreateQuestionReview.as_view({"post": "create"})),
    path("answer_review/", views.CreateAnswerReview.as_view({"post": "create"})),
    path("<int:id>/", views.QuestionView.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"}
    )),
    path("", views.QuestionView.as_view({"get": "list", "post": "create"})),
]
