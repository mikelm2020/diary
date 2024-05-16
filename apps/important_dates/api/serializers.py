from rest_framework import serializers

from apps.important_dates.models import ImportantDates


class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDates
        fields = ("important_date", "important_date_type")


class ImportantDateRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDates
        fields = ("important_date", "important_date_type")

    def save(self):
        print(f"Validated data: {self.validated_data} ")
        new_important_date = ImportantDates.objects.create(**self.validated_data)
        return new_important_date


class ImportantDateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDates
        fields = ("id", "important_date", "important_date_type")

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "important_date": instance["important_date"],
                "important_date_type": instance["important_date_type"],
            }


class ImportantDateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDates
        fields = ("important_date",)
