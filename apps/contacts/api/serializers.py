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
        if data["name"] == "" or data["last_name"] == "" or data["phones"] == "":
            raise serializers.ValidationError(
                "Debe registrar su nombre y apellido y por lo menos un telefono"
            )
        return data

    def create(self, validated_data):
        """
        Create a new contact instance and associated related objects.

        This method takes the validated data from the serializer, creates a new contact
        instance in the database, and then iterates over the related objects provided in the
        validated data to create corresponding records in the database.

        Parameters:
        validated_data (dict): A dictionary containing the validated data from the serializer.
            This data includes the contact details, as well as lists of related objects (phones, emails, etc.).

        Returns:
        contact (Contacts): The newly created contact instance.

        Raises:
        None

        """
        phones_data = validated_data.pop("phones", [])  # Get data from phones
        emails_data = validated_data.pop("emails", [])  # Get data from emails
        # Get data from addresses
        addresses_data = validated_data.pop("address", [])
        # Get data from important dates
        important_dates_data = validated_data.pop(
            "important_dates", []
        )  # Get data from related persons
        related_persons_data = validated_data.pop(
            "related_persons", []
        )  # Get data from tags
        tags_data = validated_data.pop("tags", [])

        # Create the main object (in this case, the contact)
        contact = Contacts.objects.create(**validated_data)

        for phone_data in phones_data:
            # Create each phone object related to the contact
            phone = Phones.objects.create(**phone_data)
            # Add phone to contact
            contact.phones.add(phone)

        for email_data in emails_data:
            # Create each email object related to the contact
            email = Emails.objects.create(**email_data)
            # Add email to contact
            contact.emails.add(email)

        for address_data in addresses_data:
            # Create each address object related to the contact
            address = Address.objects.create(**address_data)
            # Add address to contact
            contact.address.add(address)

        for important_date_data in important_dates_data:
            # Create each iportante date object related to the contact
            important_date = ImportantDates.objects.create(**important_date_data)
            # Add important date to contact
            contact.important_dates.add(important_date)

        for related_person_data in related_persons_data:
            # Create each related person object related to the contact
            related_person = RelatedPersons.objects.create(**related_person_data)
            # Add related person to contact
            contact.related_persons.add(related_person)

        for tag_data in tags_data:
            # Create each tag object related to the contact
            tag = Tags.objects.create(**tag_data)
            # Add tag to contact
            contact.tags.add(tag)

        return contact
