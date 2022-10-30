from django_filters import rest_framework as filters
from src.profiles.models import FatUser
from src.courses.models import  HelpUser


class UsersFilter(filters.FilterSet):
    first_login = filters.DateTimeFilter(field_name="first_login", lookup_expr="gte")

    class Meta:
        model = FatUser
        fields = ('first_login', 'coins', 'id')


class HelpUserFilter(filters.FilterSet):
    course = filters.CharFilter(field_name="lesson__course", lookup_expr="exact")

    class Meta:
        model = HelpUser
        fields = ('student', 'course', 'mentor')


