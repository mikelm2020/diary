from rest_framework import serializers

from apps.related_persons.models import RelatedPersons


class RelatedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedPersons
        fields = ("name", "related_person_type")


class RelatedPersonRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedPersons
        fields = ("name", "related_person_type")

    def save(self):
        print(f"Validated data: {self.validated_data} ")
        new_email = RelatedPersons.objects.create(**self.validated_data)
        return new_email


class RelatedPersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedPersons
        fields = ("id", "name", "related_person_type")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "name": instance["name"],
                "related_person_type": instance["related_person_type"],
            }


class RelatedPersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedPersons
        fields = ("name",)
