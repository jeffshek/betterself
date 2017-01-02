from drf_compound_fields.fields import ListOrItemField
from rest_framework import serializers

from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement
from vendors.models import Vendor


def user_viewable_objects_validator(model, user, ids_string):
    ids_string_parsed = ids_string.strip().split(',')
    user_viewable_objects = model.get_user_viewable_objects(user).values_list('id')

    not_authorized = [item for item in ids_string_parsed if int(item) not in user_viewable_objects]
    if not_authorized:
        raise serializers.ValidationError('Not authorized to view {0} for {1}'.format(not_authorized[0], user))


class VendorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    email = serializers.EmailField(max_length=254)
    url = serializers.URLField(required=False)
    uuid = serializers.UUIDField(required=False, read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model
        name = validated_data.pop('name')

        obj, created = create_model.objects.get_or_create(user=user, name=name,
            defaults=validated_data)

        if not created:
            obj.email = validated_data.get('email')
            obj.url = validated_data.get('url')
            obj.save()

        return obj


class IngredientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    half_life_minutes = serializers.IntegerField()
    uuid = serializers.UUIDField(required=False, read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model
        obj, _ = create_model.objects.get_or_create(user=user, **validated_data)
        return obj


class MeasurementReadOnlySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    short_name = serializers.CharField(max_length=100)
    is_liquid = serializers.BooleanField(default=False)
    uuid = serializers.UUIDField(required=False, read_only=True)


class IngredientCompositionReadOnlySerializer(serializers.Serializer):
    ingredient = serializers.CharField(max_length=300)
    measurement = serializers.CharField(max_length=100)
    quantity = serializers.FloatField()
    uuid = serializers.UUIDField(required=False, read_only=True)


class IngredientCompositionCreateSerializer(serializers.Serializer):
    ingredient_uuid = serializers.UUIDField(source='ingredient.uuid')
    measurement_uuid = serializers.UUIDField(source='measurement.uuid')
    quantity = serializers.FloatField()

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model

        ingredient_uuid = validated_data['ingredient']['uuid']
        ingredient = Ingredient.objects.get(uuid=ingredient_uuid)
        validated_data['ingredient'] = ingredient

        measurement_uuid = validated_data['measurement']['uuid']
        measurement = Measurement.objects.get(uuid=measurement_uuid)
        validated_data['measurement'] = measurement

        obj, _ = create_model.objects.get_or_create(user=user, **validated_data)
        return obj


class SupplementReadOnlySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    ingredient_compositions = IngredientCompositionReadOnlySerializer(many=True)
    vendor = VendorSerializer()
    uuid = serializers.UUIDField(required=False, read_only=True)


class SupplementCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    # TODO - this ListOrItemField is a hack just to make many to many associations
    # serialize. don't love it, but don't know a clean way around it just yet
    ingredient_compositions_uuids = ListOrItemField(
        serializers.UUIDField(), required=False, source='ingredient_compositions'
    )
    vendor_uuid = serializers.UUIDField(source='vendor.uuid', required=False)
    model = Supplement

    def create(self, validated_data):
        # all generated objects should have a user field
        user = self.context['request'].user
        validated_data['user'] = user

        if 'ingredient_compositions' in validated_data:
            ingredient_compositions_uuids = validated_data.pop('ingredient_compositions')
            ingredient_compositions = IngredientComposition.objects.filter(uuid__in=ingredient_compositions_uuids)
        else:
            ingredient_compositions = []

        vendor_uuid = validated_data['vendor']['uuid']
        vendor = Vendor.objects.get(uuid=vendor_uuid)
        validated_data['vendor'] = vendor

        # cannot associate many to many unless item has been saved
        supplement, _ = Supplement.objects.get_or_create(**validated_data)

        for composition in ingredient_compositions:
            supplement.ingredient_compositions.add(composition)

        return supplement
