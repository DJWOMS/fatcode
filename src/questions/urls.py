from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ListQuestionsView.as_view({
        'get': 'list'
    })),
    path('answer/<int:id>/', views.AnswerView.as_view({
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('create_answer/', views.CreateAnswerView.as_view({
        'post': 'create'
    })),
    path('<int:id>/', views.QuestionView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('question_review/', views.CreateQuestionReview.as_view({
        'post': 'create'
    })),
    path('answer_review/', views.CreateAnswerReview.as_view({
        'post': 'create'
    }))
]
