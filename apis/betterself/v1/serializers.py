from rest_framework import serializers


class IngredientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    half_life_minutes = serializers.IntegerField()


class MeasurementSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    short_name = serializers.CharField(max_length=100, null=True, blank=True)  # 'ml'
    is_liquid = serializers.BooleanField(default=False)


class IngredientCompositionSerializer(serializers.Serializer):
    pass


class SupplementProductSerializer(serializers.Serializer):
    pass
