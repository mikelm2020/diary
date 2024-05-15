from rest_framework import serializers

from apps.contacts.models import Contacts
from apps.phones.api.serializers import PhoneRegisterSerializer, PhonesSerializer
from apps.phones.models import Phones


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ("id", "name", "last_name", "phones", "user")


class ContactListSerializer(serializers.ModelSerializer):
    phones = PhonesSerializer(many=True, read_only=True)

    class Meta:
        model = Contacts
        fields = ("id", "name", "last_name", "phones")

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            phones_data = instance.phones.all()
            representation["phones"] = [phone.phone for phone in phones_data]
            return representation

        # def to_representation(self, instance):
        #     return {
        #         "id": instance["id"],
        #         "name": instance["name"],
        #         "last_name": instance["last_name"],
        #         "phone": instance["phones"],
        #     }


class ContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = (
            "name",
            "last_name",
            "phones",
        )


class ContactsRegisterSerializer(serializers.ModelSerializer):
    phones = PhoneRegisterSerializer(many=True)

    class Meta:
        model = Contacts
        fields = ["name", "last_name", "phones"]

    def validate(self, data):
        if data["name"] == "" or data["last_name"] == "" or data["phones"] == "":
            raise serializers.ValidationError("Todos los campos son obligatorios")
        return data

    def save(self, request):
        """
        Create a new contact instance.
        """
        print(f"Validated_data: {self.validated_data} ")
        print(f"usuario: {request.user.username}")
        contact = Contacts.objects.create(
            name=self.validated_data["name"],
            last_name=self.validated_data["last_name"],
            user=request.user,
        )

        for phone_data in self.validated_data["phones"]:
            print(f"phone_data: {phone_data} ")
            print(f"phones validated_data: {self.validated_data['phones']}")
            phone_number = phone_data["phone"]["number"]
            phone_type = phone_data["phone_type"]
            Phones.objects.create(phone=phone_number, phone_type=phone_type)
        return contact
