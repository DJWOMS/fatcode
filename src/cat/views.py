from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from . import models
from . import serializers


class CheckInventoryView(RetrieveAPIView):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.DetailCourseSerializer
    lookup_field = 'id'
