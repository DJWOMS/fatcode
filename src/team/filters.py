from django_filters import rest_framework as filters

from . import models


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TeamFilter(filters.FilterSet):
    project_teams = CharFilterInFilter(field_name='project_teams__toolkit__name', lookup_expr='in')

    class Meta:
        model = models.Team
        fields = ("project_teams", )
