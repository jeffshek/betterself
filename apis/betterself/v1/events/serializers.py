from django.core.exceptions import ValidationError
from rest_framework import serializers

from apis.betterself.v1.supplements.serializers import SupplementReadOnlySerializer
from events.models import INPUT_SOURCES_TUPLES
from supplements.models import Supplement


class SupplementEventCreateSerializer(serializers.Serializer):
    supplement_uuid = serializers.UUIDField(source='supplement.uuid')
    quantity = serializers.FloatField(default=1)
    time = serializers.DateTimeField()
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)
    uuid = serializers.UUIDField(required=False)

    @classmethod
    def validate_supplement_uuid(cls, value):
        # serializers check if these are valid uuid fields, but they don't
        # check that these objects should actually exist. do it here!
        try:
            Supplement.objects.get(uuid=value)
        except Supplement.DoesNotExist:
            raise ValidationError('Supplement UUID {} does not exist'.format(value))

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model

        supplement_uuid = validated_data.pop('supplement')['uuid']
        supplement = Supplement.objects.get(uuid=supplement_uuid)

        quantity = validated_data.pop('quantity')
        time = validated_data.pop('time')

        obj, _ = create_model.objects.get_or_create(user=user, quantity=quantity,
            time=time, supplement=supplement, **validated_data)
        return obj


class SupplementEventReadOnlySerializer(serializers.Serializer):
    supplement = SupplementReadOnlySerializer()
    quantity = serializers.FloatField()
    time = serializers.DateTimeField()
    source = serializers.CharField()
    uuid = serializers.UUIDField()
