from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>/', views.RetrieveQuestionView.as_view({
        'get': 'retrieve'
    })),
    path('list/', views.ListQuestionsView.as_view({
        'get': 'list'
    })),
    path('create_answer/', views.CreateAnswerView.as_view({
        'post': 'create'
    })),
    path('update_question/<int:id>/', views.UpdateQuestionView.as_view({
        'put': 'update', 'patch': 'partial_update'
    })),
    path('update_answer/<int:id>/', views.UpdateAnswerView.as_view({
        'put': 'update', 'patch': 'partial_update'
    })),
    path('delete_answer/<int:id>/', views.DestroyAnswerView.as_view({
        'delete': 'delete'
    })),
    path('delete_question/<int:id>/', views.DestroyQuestionView.as_view({
        'delete': 'delete'
    })),
    path('question_review/', views.CreateQuestionReview.as_view({
        'post': 'create'
    })),
    path('answer_review/', views.CreateAnswerReview.as_view({
        'post': 'create'
    }))
]
