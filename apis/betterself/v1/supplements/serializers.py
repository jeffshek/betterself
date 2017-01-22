from drf_compound_fields.fields import ListOrItemField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement
from vendors.models import Vendor


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
    half_life_minutes = serializers.IntegerField(required=False)
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
    ingredient = IngredientSerializer(required=True)
    measurement = MeasurementReadOnlySerializer()
    quantity = serializers.FloatField()
    uuid = serializers.UUIDField(read_only=True)


class IngredientCompositionCreateSerializer(serializers.Serializer):
    ingredient_uuid = serializers.UUIDField(source='ingredient.uuid')
    measurement_uuid = serializers.UUIDField(source='measurement.uuid', required=False)
    quantity = serializers.FloatField(required=False)
    uuid = serializers.UUIDField(required=False, read_only=True)

    def validate(self, validated_data):
        ingredient_uuid = validated_data['ingredient']['uuid']
        ingredient = Ingredient.objects.get(uuid=ingredient_uuid)
        validated_data['ingredient'] = ingredient

        if 'measurement' in validated_data:
            measurement_details = validated_data.pop('measurement')
            # measurement_details = validated_data['measurement']
            measurement_uuid = measurement_details['uuid']

            try:
                measurement = Measurement.objects.get(uuid=measurement_uuid)
            except Vendor.DoesNotExist:
                raise ValidationError('Non-required measurement UUID doesn\'t exist'.format(measurement_uuid))

            validated_data['measurement'] = measurement

        return validated_data

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model

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
    # really want to refactor all UUID looks ups to be serialized separately to do a lookup
    # to make sure that the UUID is valid before trying to create it
    vendor_uuid = serializers.UUIDField(source='vendor.uuid', required=False)
    uuid = serializers.UUIDField(required=False, read_only=True)

    model = Supplement

    def validate(self, validated_data):
        if 'vendor' in validated_data:
            vendor_details = validated_data.pop('vendor')
            vendor_uuid = vendor_details['uuid']

            try:
                vendor = Vendor.objects.get(uuid=vendor_uuid)
            except Vendor.DoesNotExist:
                raise ValidationError('Non-required vendor UUID doesn\'t exist'.format(vendor_uuid))

            validated_data['vendor'] = vendor

        if 'ingredient_compositions' in validated_data:
            ingredient_compositions_uuids = validated_data.pop('ingredient_compositions')

            if isinstance(ingredient_compositions_uuids, list):
                ingredient_compositions = IngredientComposition.objects.filter(uuid__in=ingredient_compositions_uuids)

                if ingredient_compositions.count() != len(ingredient_compositions_uuids):
                    raise ValidationError('Not all ingredient composition UUIDs were found {}'.format(
                        ingredient_compositions_uuids))
            else:
                # TODO - add a test for this, this is because of the list
                # or single situation
                ing_comp = IngredientComposition.objects.get(uuid=ingredient_compositions_uuids)
                ingredient_compositions = [ing_comp]

        else:
            ingredient_compositions = []

        validated_data['ingredient_compositions'] = ingredient_compositions

        return validated_data

    def create(self, validated_data):
        # all generated objects should have a user field
        user = self.context['request'].user
        validated_data['user'] = user
        ingredient_compositions = validated_data.pop('ingredient_compositions')

        # cannot associate many to many unless item has been saved
        supplement, _ = Supplement.objects.get_or_create(**validated_data)

        for composition in ingredient_compositions:
            supplement.ingredient_compositions.add(composition)

        return supplement
