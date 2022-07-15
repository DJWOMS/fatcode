from django.urls import path
from .views import *

urlpatterns = [
    path('list/', CourseListView.as_view())
]