from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from supplements.models import Supplement, IngredientComposition
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

    def create(self, validated_data):
        return Vendor(**validated_data)


class IngredientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    half_life_minutes = serializers.IntegerField()


class MeasurementSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    short_name = serializers.CharField(max_length=100)
    is_liquid = serializers.BooleanField(default=False)


class IngredientCompositionSerializer(serializers.Serializer):
    ingredient = serializers.CharField(max_length=300)
    measurement = serializers.CharField(max_length=100)
    quantity = serializers.FloatField()


class IngredientCompositionIDsField(serializers.RelatedField):
    """ Serializers a string of IDs of ingredient compositions """
    SERIALIZER_MODEL = IngredientComposition

    def to_representation(self, value):
        user = self.context['request'].user
        IngredientComposition.get_user_viewable_objects(user)


class SupplementReadSerializer(serializers.Serializer):
    # TD - Think of a better name than this
    name = serializers.CharField(max_length=300)
    ingredient_compositions = IngredientCompositionSerializer(many=True)
    vendor = VendorSerializer()


class SupplementCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    # if a list of ids are provided, comma split them
    ingredient_compositions_ids = serializers.CharField(required=False)
    vendor_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        # all generated objects should have a user field
        user = self.context['request'].user
        validated_data['user'] = user

        vendor_id = validated_data.pop('vendor_id', None)
        if vendor_id:
            validated_data = self._add_vendor_to_validated_data(user, validated_data, vendor_id)

        ingredient_compositions = []
        ingredient_compositions_ids = validated_data.pop('ingredient_compositions_ids', None)
        if ingredient_compositions_ids:
            ingredient_compositions = self._get_ingredient_compositions_accessible_for_user(user,
                ingredient_compositions_ids)

        # cannot associate many to many unless item has been saved
        supplement = Supplement.objects.create(**validated_data)

        for composition in ingredient_compositions:
            supplement.ingredient_compositions.add(composition)

        return supplement

    # TD - if you have to implement this again, move to base model!
    @staticmethod
    def _get_ingredient_compositions_accessible_for_user(user, ingredient_compositions_ids):
        try:
            ingredient_compositions_ids_parsed = [int(item) for item in ingredient_compositions_ids.strip().split(',')]
        except TypeError:
            raise TypeError('Invalid Ingredient Compositions Ids Entered {0}'.format(ingredient_compositions_ids))

        queryset = IngredientComposition.objects.filter(id__in=ingredient_compositions_ids_parsed).filter(
            Q(user=user) | Q(user__isnull=True))

        if not queryset.first():
            raise ValidationError('No Ingredient Composition IDs of {0} found belong to user {1}'.format(
                ingredient_compositions_ids, user.id))
        else:
            return queryset

    @staticmethod
    def _add_vendor_to_validated_data(user, validated_data, vendor_id):
        vendor = Vendor.objects.filter(id=vendor_id).filter(Q(user=user) | Q(user__isnull=True))
        if not vendor:
            raise ValidationError('No Vendor ID of {0} found belong to user {1}'.format(vendor_id, user.id))
        else:
            validated_data['vendor'] = vendor.first()

        return validated_data
