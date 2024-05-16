from rest_framework import serializers

from apps.emails.models import Emails


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ("email", "email_type")


class EmailRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ("email", "email_type")

    def save(self):
        print(f"Validated data: {self.validated_data} ")
        new_email = Emails.objects.create(**self.validated_data)
        return new_email


class EmailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ("id", "email", "email_type")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "email": instance["email"],
                "email_type": instance["email_type"],
            }


class EmailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ("email",)
