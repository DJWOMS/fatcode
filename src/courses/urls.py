from django.urls import path

from . import views

urlpatterns = [
    path('detail/<int:id>/', views.DetailCourseView.as_view(), name="course-detail"),
    path('list/', views.ListCourseView.as_view(), name="course-list"),
    path('lesson/<int:id>/', views.DetailLessonView.as_view(), name="lesson-detail"),
    path('check_work/', views.StudentWorkView.as_view(), name="check-work"),
    path('help_mentor/', views.HelpUserView.as_view(), name="help-mentor")
]
