from django.core.exceptions import ValidationError
from rest_framework import serializers

from apis.betterself.v1.supplements.serializers import SupplementReadOnlySerializer
from events.models import INPUT_SOURCES_TUPLES
from supplements.models import Supplement


def valid_daily_max_minutes(value):
    minutes_in_day = 60 * 24
    if value > minutes_in_day:
        raise serializers.ValidationError('Error - More than minutes in a day.')
    elif value < 0:
        raise serializers.ValidationError('Less than 1 is not allowed.')


class SupplementEventCreateSerializer(serializers.Serializer):
    supplement_uuid = serializers.UUIDField(source='supplement.uuid')
    quantity = serializers.FloatField(default=1)
    time = serializers.DateTimeField()
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)
    uuid = serializers.UUIDField(required=False, read_only=True)

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
        time = validated_data.pop('time')

        obj, _ = create_model.objects.get_or_create(
            user=user,
            time=time,
            supplement=supplement,
            **validated_data)

        return obj


class SupplementEventReadOnlySerializer(serializers.Serializer):
    supplement = SupplementReadOnlySerializer()
    quantity = serializers.FloatField()
    time = serializers.DateTimeField()
    source = serializers.CharField()
    uuid = serializers.UUIDField()


class ProductivityLogReadSerializer(serializers.Serializer):
    very_productive_time_minutes = serializers.IntegerField(required=False)
    productive_time_minutes = serializers.IntegerField(required=False)
    neutral_time_minutes = serializers.IntegerField(required=False)
    distracting_time_minutes = serializers.IntegerField(required=False)
    very_distracting_time_minutes = serializers.IntegerField(required=False)
    date = serializers.DateField()
    uuid = serializers.UUIDField()


class ProductivityLogCreateSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, read_only=True)

    very_productive_time_minutes = serializers.IntegerField(required=False, validators=[valid_daily_max_minutes])
    productive_time_minutes = serializers.IntegerField(required=False, validators=[valid_daily_max_minutes])
    neutral_time_minutes = serializers.IntegerField(required=False, validators=[valid_daily_max_minutes])
    distracting_time_minutes = serializers.IntegerField(required=False, validators=[valid_daily_max_minutes])
    very_distracting_time_minutes = serializers.IntegerField(required=False, validators=[valid_daily_max_minutes])
    date = serializers.DateField()

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model
        date = validated_data.pop('date')

        obj, created = create_model.objects.get_or_create(
            user=user,
            date=date,
            **validated_data)

        return obj
