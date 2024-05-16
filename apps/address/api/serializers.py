from rest_framework import serializers

from apps.address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("address", "address_type")


class AddressRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("address", "address_type")

    def save(self):
        print(f"Validated data: {self.validated_data} ")
        new_address = Address.objects.create(**self.validated_data)
        return new_address


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "address", "address_type")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "address": instance["address"],
                "address_type": instance["address_type"],
            }


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("address",)
