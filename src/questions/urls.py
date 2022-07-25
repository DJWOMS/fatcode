from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>/', views.RetrieveQuestionView.as_view()),
    path('list/', views.ListQuestionsView.as_view()),
]
