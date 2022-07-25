from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>/', views.DetailCourseView.as_view()),
    path('list/', views.ListCourseView.as_view()),
    path('lesson/<int:id>/', views.DetailLessonView.as_view()),
    path('check_work/', views.StudentWorkView.as_view()),
    path('help_mentor/', views.HelpUserView.as_view())
]
