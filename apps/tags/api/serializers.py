from rest_framework import serializers

from apps.tags.models import Tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("tag",)


class TagRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("tag",)

    def save(self):
        print(f"Validated data: {self.validated_data} ")
        new_tag = Tags.objects.create(**self.validated_data)
        return new_tag


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = (
            "id",
            "tag",
        )

        def to_representation(self, instance):
            return {
                "id": instance["id"],
                "tag": instance["tag"],
            }


class TagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("tag",)
