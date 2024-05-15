from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.models import User


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {"bad_token": ("El Token ha expirado o es inválido")}

    def validate(self, attrs):
        """
        Validate the input attributes.

        This method validates the input attributes and sets the 'token' attribute to the value of the 'refresh' attribute from the input.

        Args:
        attrs (dict): A dictionary containing the input attributes.

        Returns:
        dict: The validated input attributes.

        """
        self.token = attrs["refresh"]
        return attrs

    def save(self, *args, **kwargs):
        """
        Blacklist the refresh token.

        This method attempts to blacklist the refresh token provided in the request. If the token is valid, it is blacklisted, and if it is invalid or has expired, a TokenError is raised.

        Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Raises:
        TokenError: If the provided refresh token is invalid or has expired.

        Returns:
        None
        """
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
