from rest_framework import serializers

from supplements.models import Supplement


class VendorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    email = serializers.EmailField(max_length=254)
    url = serializers.URLField()


class IngredientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    half_life_minutes = serializers.IntegerField()


class MeasurementSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    short_name = serializers.CharField(max_length=100)
    is_liquid = serializers.BooleanField(default=False)


class IngredientCompositionSerializer(serializers.Serializer):
    ingredient_name = serializers.CharField(max_length=300)
    measurement_name = serializers.CharField(max_length=100)
    quantity = serializers.FloatField()


class SupplementSerializer(serializers.Serializer):
    ingredient_names = serializers.CharField(max_length=600, source='ingredient_compositions')
    name = serializers.CharField(max_length=300)
    vendor_name = serializers.CharField(max_length=300, source='vendor')

    def create(self, validated_data):
        # except for very specific data, all generated objects should have a user field
        user = self.context['request'].user
        validated_data['user'] = user
        return Supplement(**validated_data)
