from django_filters import rest_framework

from apps.contacts.models import Contacts
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


class ContactFilterSet(rest_framework.FilterSet):
    class Meta:
        model = Contacts
        fields = (
            "name",
            "last_name",
            "phones",
            "user",
        )
