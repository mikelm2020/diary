from rest_framework import serializers

from apps.address.api.serializers import AddressSerializer
from apps.address.models import Address
from apps.contacts.models import Contacts
from apps.emails.api.serializers import EmailSerializer
from apps.emails.models import Emails
from apps.important_dates.api.serializers import ImportantDateSerializer
from apps.important_dates.models import ImportantDates
from apps.phones.api.serializers import PhonesSerializer
from apps.phones.models import Phones
from apps.related_persons.api.serializers import RelatedPersonSerializer
from apps.related_persons.models import RelatedPersons
from apps.tags.api.serializers import TagSerializer
from apps.tags.models import Tags


class ContactSerializer(serializers.ModelSerializer):
    phones = PhonesSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True, read_only=True)
    important_dates = ImportantDateSerializer(many=True, read_only=True)
    related_persons = RelatedPersonSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Contacts
        fields = (
            "name",
            "last_name",
            "company",
            "phones",
            "emails",
            "address",
            "website",
            "important_dates",
            "related_persons",
            "sip",
            "notes",
            "tags",
        )


class ContactListSerializer(serializers.ModelSerializer):
    phones = PhonesSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True, read_only=True)
    important_dates = ImportantDateSerializer(many=True, read_only=True)
    related_persons = RelatedPersonSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Contacts
        fields = (
            "id",
            "name",
            "last_name",
            "company",
            "phones",
            "emails",
            "address",
            "website",
            "important_dates",
            "related_persons",
            "sip",
            "notes",
            "tags",
        )

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            phones_data = instance.phones.all()
            representation["phones"] = [phone.phone for phone in phones_data]
            emails_data = instance.emails.all()
            representation["emails"] = [email.email for email in emails_data]
            addressses_data = instance.address.all()
            representation["address"] = [address.address for address in addressses_data]
            important_dates_data = instance.important_dates.all()
            representation["important_dates"] = [
                important_date.important_date for important_date in important_dates_data
            ]
            related_persons_data = instance.related_persons.all()
            representation["related_persons"] = [
                related_person.related_person for related_person in related_persons_data
            ]
            tags_data = instance.tags.all()
            representation["tags"] = [tag.tag for tag in tags_data]
            return representation


class ContactUpdateSerializer(serializers.ModelSerializer):
    phones = PhonesSerializer(many=True)
    emails = EmailSerializer(many=True)
    address = AddressSerializer(many=True)
    important_dates = ImportantDateSerializer(many=True)
    related_persons = RelatedPersonSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Contacts
        fields = (
            "name",
            "last_name",
            "company",
            "phones",
            "emails",
            "address",
            "website",
            "important_dates",
            "related_persons",
            "sip",
            "notes",
            "tags",
            "is_active",
        )


class ContactsRegisterSerializer(serializers.ModelSerializer):
    phones = PhonesSerializer(many=True)
    emails = EmailSerializer(many=True)
    address = AddressSerializer(many=True)
    important_dates = ImportantDateSerializer(many=True)
    related_persons = RelatedPersonSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Contacts
        fields = (
            "name",
            "last_name",
            "company",
            "phones",
            "emails",
            "address",
            "website",
            "important_dates",
            "related_persons",
            "sip",
            "notes",
            "tags",
        )

    def validate(self, data):
        print(f"Esta es la Data: {data}")
        if data["name"] == "" or data["last_name"] == "" or data["phones"] == "":
            raise serializers.ValidationError(
                "Debe registrar su nombre y apellido y por lo menos un telefono"
            )
        return data

    def create(self, validated_data):
        """
        Create a new contact instance and associated phone numbers.

        This method takes the validated data from the serializer, creates a new contact
        instance in the database, and then iterates over the phone numbers provided in the
        validated data to create corresponding phone records in the database.

        Parameters:
        None

        Returns:
        contact (Contacts): The newly created contact instance.

        Raises:
        None

        """
        # print(f"Validated_data: {self.validated_data} ")
        # contact = super().save(**kwargs)
        # # contact = Contacts.objects.create(
        # #     name=self.validated_data["name"],
        # #     last_name=self.validated_data["last_name"],
        # #     user=self.validated_data["user"],
        # # )

        # # Associates the phones to created contact
        # phones_data = self.validated_data.get("phones", [])
        # for phone_data in phones_data:
        #     phone_number = phone_data["phone"]["phone"]
        #     phone_type = phone_data["phone_type"]
        #     Phones.objects.create(
        #         contact=contact, phone=phone_number, phone_type=phone_type
        #     )

        # # Associates the emails to created contact
        # emails_data = self.validated_data.get("emails", [])
        # for email_data in emails_data:
        #     email = email_data["email"]
        #     email_type = email_data["email_type"]
        #     Emails.objects.create(contact=contact, email=email, email_type=email_type)

        # # Associates the address to created contact
        # addresses_data = self.validated_data.get("address", [])
        # for address_data in addresses_data:
        #     address = address_data["address"]
        #     address_type = address_data["address_type"]
        #     Address.objects.create(
        #         contact=contact, address=address, address_type=address_type
        #     )

        # # Associates the important dates to created contact
        # important_dates_data = self.validated_data.get("important_dates", [])
        # for important_date_data in important_dates_data:
        #     important_date = important_date_data["important_date"]
        #     important_date_type = important_date_data["important_date_type"]
        #     ImportantDates.objects.create(
        #         contact=contact,
        #         important_date=important_date,
        #         important_date_type=important_date_type,
        #     )

        # # Associates the related persons to created contact
        # related_persons_data = self.validated_data.get("related_persons", [])
        # for related_person_data in related_persons_data:
        #     name = related_person_data["name"]
        #     related_person_type = related_person_data["related_person_type"]
        #     RelatedPersons.objects.create(
        #         contact=contact,
        #         name=name,
        #         related_person_type=related_person_type,
        #     )

        # # Associates the tags to created contact
        # tags_data = self.validated_data.get("tags", [])
        # for tag_data in tags_data:
        #     tag = tag_data["tag"]
        #     Tags.objects.create(contact=contact, tag=tag)

        # return contact
        # Manejar la creación de objetos relacionados (nested objects) aquí
        phones_data = validated_data.pop("phones", [])  # Obtener datos de los teléfonos
        emails_data = validated_data.pop("emails", [])  # Obtener datos de los emails
        addresses_data = validated_data.pop(
            "address", []
        )  # Obtener datos de los emails
        important_dates_data = validated_data.pop(
            "important_dates", []
        )  # Obtener datos de los emails
        related_persons_data = validated_data.pop(
            "related_persons", []
        )  # Obtener datos de los emails
        tags_data = validated_data.pop("tags", [])  # Obtener datos de los emails

        # Crea el objeto principal (en este caso, el contacto)
        contact = Contacts.objects.create(**validated_data)

        # Crea los objetos relacionados (en este caso, los teléfonos y emails)
        for phone_data in phones_data:
            # Crea cada objeto de teléfono relacionado con el contacto
            # Aquí debes adaptar esto según cómo estén definidos tus modelos
            phone = Phones.objects.create(**phone_data)
            # Agregar el teléfono al contacto
            contact.phones.add(phone)

        for email_data in emails_data:
            # Crea cada objeto de email relacionado con el contacto
            # Aquí debes adaptar esto según cómo estén definidos tus modelos
            email = Emails.objects.create(**email_data)
            # Agregar el teléfono al contacto
            contact.emails.add(email)

        for address_data in addresses_data:
            # Crea cada objeto de email relacionado con el contacto
            # Aquí debes adaptar esto según cómo estén definidos tus modelos
            address = Address.objects.create(**address_data)
            # Agregar el teléfono al contacto
            contact.address.add(address)

        for important_date_data in important_dates_data:
            # Crea cada objeto de email relacionado con el contacto
            # Aquí debes adaptar esto según cómo estén definidos tus modelos
            important_date = ImportantDates.objects.create(**important_date_data)
            # Agregar el teléfono al contacto
            contact.important_dates.add(important_date)

        for related_person_data in related_persons_data:
            # Crea cada objeto de email relacionado con el contacto
            # Aquí debes adaptar esto según cómo estén definidos tus modelos
            related_person = RelatedPersons.objects.create(**related_person_data)
            # Agregar el teléfono al contacto
            contact.related_persons.add(related_person)

        for tag_data in tags_data:
            # Crea cada objeto de email relacionado con el contacto
            # Aquí debes adaptar esto según cómo estén definidos tus modelos
            tag = Tags.objects.create(**tag_data)
            # Agregar el teléfono al contacto
            contact.tags.add(tag)

        return contact
