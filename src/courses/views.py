from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
