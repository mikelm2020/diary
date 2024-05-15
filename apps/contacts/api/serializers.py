from rest_framework import serializers

from apps.contacts.models import Contacts


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


class ContactsRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Contacts
        fields = ["username", "email", "password", "password2", "is_owner"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """
        Ensure the passwords are the same and meet any other validation criteria.
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."}
            )
        return data

    def save(self, request):
        """
        Create a new user instance.
        """
        user = Contacts(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            is_owner=self.validated_data.get("is_owner", False),
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user
