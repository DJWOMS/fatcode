from rest_framework import routers
from django.urls import path, include

from .views import CourseModelView, LessonModelView, StudentWorkView, HelpUserView

router = routers.SimpleRouter()

router.register(r'courses', CourseModelView),
router.register(r'lessons', LessonModelView),
router.register(r'works', StudentWorkView),
router.register(r'helps', HelpUserView)

urlpatterns = [
    path('', include(router.urls)),
]
