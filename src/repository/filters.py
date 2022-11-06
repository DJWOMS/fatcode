from django_filters import FilterSet
from django_filters import DateTimeFilter, NumberFilter

from . import models


class ProjectFilter(FilterSet):
    date_min = DateTimeFilter(field_name="last_commit", lookup_expr="gte")
    date_max = DateTimeFilter(field_name="last_commit", lookup_expr="lte")
    star_min = NumberFilter(field_name="star", lookup_expr="gte")
    star_max = NumberFilter(field_name="star", lookup_expr="lte")
    fork_min = NumberFilter(field_name="fork", lookup_expr="gte")
    fork_max = NumberFilter(field_name="fork", lookup_expr="lte")
    commit_count_min = NumberFilter(field_name="commit", lookup_expr="gte")
    commit_count_max = NumberFilter(field_name="commit", lookup_expr="lte")

    class Meta:
        model = models.Project
        fields = (
            "name",
            "toolkit",
            "category",
            "date_min",
            "date_max",
            "star_min",
            "star_max",
            "fork_min",
            "fork_max",
            "commit_count_min",
            "commit_count_max",
            "user",
            "teams"
        )
