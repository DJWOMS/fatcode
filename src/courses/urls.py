from django.urls import path
from .views import *

urlpatterns = [
    path('detail/<slug:slug>/', DetailCourseView.as_view()),
    path('list/', ListCourseView.as_view()),
    path('lesson/<slug:slug>/', DetailLessonView.as_view())
]