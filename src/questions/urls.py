from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ListQuestionsView.as_view({
        'get': 'list'
    }), name="question-list"),
    path('answer/<int:id>/', views.AnswerView.as_view({
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name="answer"),
    path('create_answer/', views.CreateAnswerView.as_view({
        'post': 'create'
    }), name="create-answer"),
    path('<int:id>/', views.QuestionView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name="question"),
    path('question_review/', views.CreateQuestionReview.as_view({
        'post': 'create'
    }), name="question-review"),
    path('answer_review/', views.CreateAnswerReview.as_view({
        'post': 'create'
    }), name="answer-review")
]
