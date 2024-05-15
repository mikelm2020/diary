from rest_framework import serializers

from apps.contacts.models import Contacts
from apps.phones.api.serializers import PhoneRegisterSerializer


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ("id", "name", "last_name", "phone", "user")


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ("id", "name", "last_name", "phone", "user")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "name": instance["name"],
                "last_name": instance["last_name"],
                "phone": instance["phone"],
                "user": instance["user"],
            }


class ContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = (
            "name",
            "last_name",
            "phone",
        )


class ContactsRegisterSerializer(serializers.ModelSerializer):
    phone = PhoneRegisterSerializer

    class Meta:
        model = Contacts
        fields = ["name", "last_name", "phone", "user"]

    def validate(self, data):
        if (
            data["name"] == ""
            or data["last_name"] == ""
            or data["phone"] == ""
            or data["user"] == ""
        ):
            raise serializers.ValidationError("Todos los campos son obligatorios")

    def save(self, request):
        """
        Create a new contact instance.
        """
        contact = Contacts(
            name=self.validated_data["name"],
            last_name=self.validated_data["last_name"],
            phone=self.validated_data["phone"],
            user=request.user,
        )
        contact.save()
        return contact
