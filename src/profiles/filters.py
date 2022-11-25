from django_filters import rest_framework as filters

from . import models


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ToolkitFilter(filters.FilterSet):
    toolkit = CharFilterInFilter(field_name='toolkit__name', lookup_expr='in')

    class Meta:
        model = models.Questionnaire
        fields = ("toolkit", )
