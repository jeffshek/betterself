from rest_framework import serializers


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
    # robustness principle ... for key relationships,
    # allow name or id to use as a lookup
    ingredient_name = serializers.CharField(max_length=300)
    ingredient_id = serializers.IntegerField()
    measurement_name = serializers.CharField(max_length=100)
    measurement_id = serializers.IntegerField()
    quantity = serializers.FloatField()


class SupplementProductSerializer(serializers.Serializer):
    # take a list of ingredients
    # accept both ids or names
    ingredient_names = serializers.CharField(max_length=600)
    # if > 100 character of ids ... something has to be wrong
    ingredient_ids = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=300)

    vendor_name = serializers.CharField(max_length=300)
    vendor_id = serializers.IntegerField()
