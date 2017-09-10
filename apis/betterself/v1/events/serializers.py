from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.generics import get_object_or_404

from betterself.utils.date_utils import get_current_date_months_ago
from events.models import INPUT_SOURCES_TUPLES, UserActivity
from supplements.models import Supplement


def valid_daily_max_minutes(value):
    minutes_in_day = 60 * 24
    if value > minutes_in_day:
        raise serializers.ValidationError('Error - More than minutes in a day.')
    elif value < 0:
        raise serializers.ValidationError('Less than 1 is not allowed.')


class SupplementEventCreateUpdateSerializer(serializers.Serializer):
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

    def update(self, instance, validated_data):
        if 'supplement' in validated_data:
            supplement_uuid = validated_data.get('supplement')['uuid']
            supplement = get_object_or_404(Supplement, uuid=supplement_uuid)
            instance.supplement = supplement

        instance.source = validated_data.get('source', instance.source)
        instance.duration_minutes = validated_data.get('duration_minutes', instance.duration_minutes)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance


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
    is_all_day_activity = serializers.BooleanField(required=False)

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
    is_all_day_activity = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        # Maybe you're doing this wrong ... don't think you should need to do all of this
        instance.name = validated_data.get('name', instance.name)
        instance.is_significant_activity = validated_data.get('is_significant_activity',
                                                              instance.is_significant_activity)
        instance.is_negative_activity = validated_data.get('is_negative_activity', instance.is_negative_activity)
        instance.is_all_day_activity = validated_data.get('is_all_day_activity', instance.is_all_day_activity)
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

    def update(self, instance, validated_data):
        if 'user_activity' in validated_data:
            try:
                user_activity_uuid = validated_data['user_activity']['uuid']
                user_activity = UserActivity.objects.get(uuid=user_activity_uuid, user=instance.user)
            except ObjectDoesNotExist:
                raise ValidationError('Invalid User Activity UUID Entered')

            instance.user_activity = user_activity

        instance.user_activity_uuid = validated_data.get('user_activity', instance.user_activity.uuid)
        instance.duration_minutes = validated_data.get('duration_minutes', instance.duration_minutes)
        instance.time = validated_data.get('time', instance.time)
        instance.source = validated_data.get('source', instance.source)
        instance.save()
        return instance


class UserActivityEventReadSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    user_activity = UserActivitySerializer()
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)
    duration_minutes = serializers.IntegerField()
    time = serializers.DateTimeField()


class SleepActivityReadSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)


class SleepActivityCreateSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, read_only=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)

    def validate(self, data):
        """
        Check that start_end/end_times are valid
        """
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError('End time must occur after start')

        return data

    def create(self, validated_data):
        create_model = self.context['view'].model
        user = self.context['request'].user

        obj, created = create_model.objects.update_or_create(
            user=user,
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            defaults=validated_data)

        return obj


class ProductivityLogRequestParametersSerializer(serializers.Serializer):
    start_date = serializers.DateField(default=get_current_date_months_ago(3))
    cumulative_window = serializers.IntegerField(default=1, min_value=1, max_value=365 * 3)


class SupplementLogRequestParametersSerializer(serializers.Serializer):
    start_date = serializers.DateField(default=get_current_date_months_ago(3))
    frequency = serializers.ChoiceField(['daily', None], default=None)
    # this is a bit tricky to explain, but if true it means to always have the results for any daily frequencies
    # to include the entire date_range from start end date range, which will result in a lot of null/empty data
    complete_date_range_in_daily_frequency = serializers.BooleanField(default=False)

    def validate(self, validated_data):
        if not validated_data['frequency'] and validated_data['complete_date_range_in_daily_frequency']:
            raise ValidationError('If there is no frequency, results should not enclose all date ranges between start '
                                  'and ending periods')

        return validated_data
