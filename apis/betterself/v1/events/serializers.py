from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import CharField

from events.models import INPUT_SOURCES_TUPLES, UserActivity
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
    supplement_name = CharField(source='supplement.name', read_only=True, required=False)
    duration_minutes = serializers.IntegerField(default=0)

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

        obj, _ = create_model.objects.update_or_create(
            user=user,
            time=time,
            supplement=supplement,
            defaults=validated_data
        )

        return obj


class SupplementEventReadOnlySerializer(serializers.Serializer):
    supplement_name = CharField(source='supplement.name')
    quantity = serializers.FloatField()
    time = serializers.DateTimeField()
    source = serializers.CharField()
    uuid = serializers.UUIDField()
    duration_minutes = serializers.IntegerField()


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

        obj, created = create_model.objects.update_or_create(
            user=user,
            date=date,
            defaults=validated_data)

        return obj


class UserActivitySerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, read_only=True)
    name = serializers.CharField()
    is_significant_activity = serializers.BooleanField(required=False)
    is_negative_activity = serializers.BooleanField(required=False)

    def create(self, validated_data):
        create_model = self.context['view'].model
        user = self.context['request'].user
        name = validated_data.pop('name')

        obj, created = create_model.objects.update_or_create(
            user=user,
            name=name,
            defaults=validated_data)

        return obj


class UserActivityUpdateSerializer(serializers.Serializer):
    """
    The create and update serializers "could" be combined, but I rather
    be explicit separation for now, I can combine them later -- just don't want to build
    tests that assume they're nested.
    """
    uuid = serializers.UUIDField()
    name = serializers.CharField(required=False)
    is_significant_activity = serializers.BooleanField(required=False)
    is_negative_activity = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_significant_activity = validated_data.get('is_significant_activity',
                                                              instance.is_significant_activity)
        instance.is_negative_activity = validated_data.get('is_negative_activity', instance.is_negative_activity)
        instance.save()
        return instance


class UserActivityEventCreateSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, read_only=True)
    # We send back user_activity_uuid after an event is created to serialize correctly
    user_activity = UserActivitySerializer(required=False, read_only=True)
    user_activity_uuid = serializers.UUIDField(source='user_activity.uuid')
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)
    duration_minutes = serializers.IntegerField(default=0)
    time = serializers.DateTimeField()

    def create(self, validated_data):
        create_model = self.context['view'].model
        user = self.context['request'].user

        activity_uuid = validated_data.pop('user_activity')['uuid']
        user_activity = UserActivity.objects.get(uuid=activity_uuid)
        time = validated_data.pop('time')

        obj, created = create_model.objects.update_or_create(
            user=user,
            user_activity=user_activity,
            time=time,
            defaults=validated_data)

        return obj


class UserActivityEventReadSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    user_activity = UserActivitySerializer()
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)
    duration_minutes = serializers.IntegerField()
    time = serializers.DateTimeField()
