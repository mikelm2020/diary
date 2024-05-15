from django_filters import rest_framework

from apps.users.models import User


class UserFilterSet(rest_framework.FilterSet):
    class Meta:
        model = User
        fields = ("username",)
