from rest_framework import serializers

from apps.users.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "username"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

        def create(self, validated_data):
            user = User(**validated_data)
            user.set_password(validated_data["password"])
            user.save()
            return user

    def validate_password(self, value):
        """
        Validate the length of the password.

        Args:
        value (str): The password value to be validated.

        Returns:
        str: The validated password value if it meets the validation criteria.

        Raises:
        serializers.ValidationError: If the password length is less than 8 characters.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )
        return value


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "username": instance["username"],
            }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(
        max_length=128, min_length=8, write_only=True
    )

    def validate(self, data):
        """
        Validate the password and password confirmation.

        Args:
        data (dict): A dictionary containing the password and password confirmation.

        Returns:
        dict: The validated data if the password and password confirmation meet the validation criteria.

        Raises:
        serializers.ValidationError: If the password length is less than 8 characters or if the password and password confirmation do not match.
        """
        if len(data["password"]) < 8 or len(data["password_confirm"]) < 8:
            raise serializers.ValidationError(
                {"La contraseña debe tener por lo menos 8 caracteres."}
            )
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Ambas contraseñas deben ser iguales"}
            )
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
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
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user
