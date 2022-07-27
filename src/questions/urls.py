from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>/', views.RetrieveQuestionView.as_view()),
    path('list/', views.ListQuestionsView.as_view()),
    path('create_answer/', views.CreateAnswerView.as_view()),
    path('update_question/<int:id>/', views.UpdateQuestionView.as_view()),
    path('update_answer/<int:id>/', views.UpdateAnswerView.as_view()),
    path('delete_answer/<int:id>/', views.DestroyAnswerView.as_view()),
    path('delete_question/<int:id>/', views.DestroyQuestionView.as_view()),
    path('question_review/', views.CreateQuestionReview.as_view()),
    path('answer_review/', views.CreateAnswerReview.as_view())
]
