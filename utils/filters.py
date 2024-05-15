from django_filters import rest_framework

from apps.phones.models import Phones
from apps.users.models import User


class UserFilterSet(rest_framework.FilterSet):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class PhoneFilterSet(rest_framework.FilterSet):
    class Meta:
        model = Phones
        fields = (
            "phone",
            "phone_type",
        )
