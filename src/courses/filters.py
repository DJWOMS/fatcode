from django_filters import rest_framework as filters
from .models import Course


class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ('name', 'tags', 'category')
