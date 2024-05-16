from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.phones.models import Phones


class PhoneNumberSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="MX")


class PhonesSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region="MX")

    class Meta:
        model = Phones
        fields = ("phone", "phone_type")


class PhoneRegisterSerializer(serializers.ModelSerializer):
    phone = PhoneNumberSerializer()

    class Meta:
        model = Phones
        fields = ("phone", "phone_type")

    def save(self):
        print(f"Validated data: {self.validated_data} ")
        new_phone = Phones.objects.create(**self.validated_data)
        return new_phone


class PhoneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phones
        fields = ("id", "phone", "phone_type")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "phone": instance["phone"],
                "phone_type": instance["phone_type"],
            }


class PhoneUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phones
        fields = ("phone",)
