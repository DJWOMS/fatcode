from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>/', views.RetrieveQuestionView.as_view()),
    path('list/', views.ListQuestionsView.as_view()),
    path('create_answer/', views.CreateAnswerView.as_view()),
    path('update_question/<int:id>/', views.UpdateQuestionView.as_view()),
    path('update_answer/<int:id>/', views.UpdateAnswerView.as_view())
]
