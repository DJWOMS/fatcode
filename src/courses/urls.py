from django.urls import path
from .views import *

urlpatterns = [
    path('detail/<int:id>/', DetailCourseView.as_view()),
    path('list/', ListCourseView.as_view()),
    path('lesson/<int:id>/', DetailLessonView.as_view()),
]