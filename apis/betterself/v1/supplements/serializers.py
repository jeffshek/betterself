from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.conf import settings

from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement, UserSupplementStack, \
    UserSupplementStackComposition
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
                raise ValidationError('Non-required Measurement UUID doesn\'t exist'.format(measurement_uuid))

            validated_data['measurement'] = measurement

        return validated_data

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model

        obj, _ = create_model.objects.get_or_create(user=user, **validated_data)
        return obj


class SupplementReadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    ingredient_compositions = IngredientCompositionReadOnlySerializer(many=True)
    uuid = serializers.UUIDField(required=False, read_only=True)
    created = serializers.DateTimeField()


class SimpleUUIDSerializer(serializers.Serializer):
    """
    All it does is verify UUID validity
    """
    uuid = serializers.UUIDField()


class SupplementCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    ingredient_compositions = SimpleUUIDSerializer(many=True, required=False)
    uuid = serializers.UUIDField(required=False, read_only=True)
    created = serializers.DateTimeField(required=False)

    def validate(self, validated_data):
        if 'ingredient_compositions' in validated_data:
            ingredient_compositions = validated_data.pop('ingredient_compositions')
            ingredient_compositions_uuids = [item['uuid'] for item in ingredient_compositions]

            ingredient_compositions = IngredientComposition.objects.filter(uuid__in=ingredient_compositions_uuids)

            if ingredient_compositions.count() != len(ingredient_compositions_uuids):
                raise ValidationError('Not all ingredient composition UUIDs were found {}'.format(
                    ingredient_compositions_uuids))

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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

        # if compositions in the data, clear out any existing compositions that might have been there
        # and reset it with any new ingredient compositions
        if 'ingredient_compositions' in validated_data:
            instance.ingredient_compositions.clear()

            for composition in validated_data['ingredient_compositions']:
                instance.ingredient_compositions.add(composition)

        instance.save()
        return instance


class UserSupplementStackCompositionReadSerializer(serializers.ModelSerializer):
    # supplement read serializers get the ingredient compositions, which maybe unnecessary
    supplement = SupplementReadSerializer()

    class Meta:
        model = UserSupplementStackComposition
        fields = ('supplement', 'quantity', 'uuid')


class UserSupplementStackReadSerializer(serializers.ModelSerializer):
    compositions = UserSupplementStackCompositionReadSerializer(many=True)

    class Meta:
        model = UserSupplementStack
        fields = ('name', 'compositions', 'uuid', 'created')


class UserSupplementStackCompositionCreateSerializer(serializers.Serializer):
    supplement_uuid = serializers.UUIDField(required=True, source='supplement.uuid')
    quantity = serializers.FloatField(default=1)


class UserSupplementStackCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    compositions = UserSupplementStackCompositionCreateSerializer(many=True)
    uuid = serializers.UUIDField(required=False, read_only=True)

    def validate_compositions(self, data):
        # for updates and testing, a user is often passed via context
        user = self.context.get('user') or self.context['request'].user

        supplement_uuids = [item['supplement']['uuid'] for item in data]
        if settings.TESTING:  # do a more thorough check for production
            supplements = Supplement.objects.filter(uuid__in=supplement_uuids)
        else:
            supplements = Supplement.objects.filter(uuid__in=supplement_uuids, user=user)

        if supplements.count() != len(supplement_uuids):
            raise ValidationError('Not all supplements UUIDs were found {}'.format(supplement_uuids))

        return data

    @staticmethod
    def _create_compositions_from_validated_data(stack, compositions_data):
        user = stack.user

        for composition in compositions_data:
            supplement = Supplement.objects.get(uuid=composition['supplement']['uuid'])
            quantity = composition['quantity']

            UserSupplementStackComposition.objects.update_or_create(stack=stack, supplement=supplement, user=user,
                defaults={'quantity': quantity})

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        name = validated_data['name']

        # cannot associate foreign key dependencies until instance has been created
        compositions = validated_data.pop('compositions')

        stack, _ = UserSupplementStack.objects.get_or_create(user=user, name=name)
        self._create_compositions_from_validated_data(stack, compositions)

        return stack

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        compositions = validated_data.get('compositions', [])

        if compositions:
            instance.compositions.all().delete()
            self._create_compositions_from_validated_data(instance, compositions)

        instance.save()
        return instance
