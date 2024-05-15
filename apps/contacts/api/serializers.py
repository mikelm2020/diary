from rest_framework import serializers

from apps.contacts.models import Contacts
from apps.phones.api.serializers import PhoneRegisterSerializer


class CustomContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ("username", "id")


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ("username", "email", "password")

        def create(self, validated_data):
            user = Contacts(**validated_data)
            user.set_password(validated_data["password"])
            user.save()
            return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )
        return value


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ("id", "username", "email")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "username": instance["username"],
                "email": instance["email"],
            }


class ContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ("email",)


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
