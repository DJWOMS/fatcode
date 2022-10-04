from django_filters import rest_framework as filters
from .models import Project


class ProjectFilter(filters.FilterSet):
    last_commit = filters.DateTimeFilter(field_name='last_commit', lookup_expr='date__gte')

    class Meta:
        model = Project
        fields = ['name']
