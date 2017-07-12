import pandas as pd
import numpy as np

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import CharField

from constants import SLEEP_CUTOFF_TIME
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


def round_timestamp_to_sleep_date(timeseries):
    """
    Not my proudest function ... this isn't as efficient as it could be, but struggling
    with some pandas syntax to find the perfect pandas one-line

    This can be much more performant, but need time to sit down and figure it out
    """
    sleep_dates = []
    for value in timeseries:
        if value.hour < SLEEP_CUTOFF_TIME:
            result = value - pd.DateOffset(days=1)
        else:
            result = value

        sleep_dates.append(result)

    index = pd.DatetimeIndex(sleep_dates)
    return index


# TODO - move these to analytics / dataframe - builders
class SleepActivityDataframeBuilder(object):
    """
    Custom serializer to parse sleep logs in a meaningful way

    Returns a dataframe of sleep activity
    """
    def __init__(self, queryset):
        self.sleep_activities = queryset
        try:
            self.user = self.sleep_activities[0].user
        except IndexError:
            self.user = None

    def get_sleep_history(self):
        if not self.user:
            return pd.Series()

        user_timezone = self.user.pytz_timezone

        sleep_activities_values = self.sleep_activities.values('start_time', 'end_time')
        sleep_activity_normalized_timezones = []
        for record in sleep_activities_values:
            record_normalized = {key: user_timezone.normalize(value) for key, value in record.items()}
            sleep_activity_normalized_timezones.append(record_normalized)

        # for each given 24 hour period (ending at 11AM)
        # Lot of mental debate here between calculating the sleep one gets from monday 10PM to tuesday 6AM which
        # date it should be attributed to ... aka either a Monday or Tuesday night.
        # I've decided to lean toward calculating that as Monday night
        dataframe = pd.DataFrame.from_records(sleep_activity_normalized_timezones)
        dataframe['sleep_time'] = dataframe['end_time'] - dataframe['start_time']

        sleep_index = round_timestamp_to_sleep_date(dataframe['end_time'])
        sleep_series = pd.Series(dataframe['sleep_time'].values, index=sleep_index)

        # get the sum of time slept during days (so this includes naps)
        # the result is timedeltas though, so convert below
        sleep_aggregate = sleep_series.resample('D').sum()

        # change from timedeltas to minutes, otherwise json response of timedelta is garbage
        sleep_aggregate = sleep_aggregate / np.timedelta64(1, 'm')
        sleep_aggregate.name = 'Sleep Minutes'
        return sleep_aggregate


class UserActivityEventDataframeBuilder(object):
    def __init__(self, queryset):
        self.user_activities = queryset

        try:
            self.user = self.user_activities[0].user
        except IndexError:
            self.user = None

    def get_user_activity_events(self):
        activity_events_values = self.user_activities.values('time', 'user_activity__name')

        if not self.user:
            return pd.DataFrame()

        user_timezone = self.user.pytz_timezone

        time_index = [item['time'].astimezone(user_timezone).date() for item in activity_events_values]
        time_index_localized = pd.DatetimeIndex(time_index).tz_localize(user_timezone)
        activity_names = [item['user_activity__name'] for item in activity_events_values]

        df = pd.DataFrame({
            'time': time_index_localized,
            'activity': activity_names,
            'value': 1
        })

        # switch to a flattened history of user activity dataframe instead
        df = df.pivot_table(index=pd.DatetimeIndex(df['time']), values='value', columns='activity', aggfunc=np.sum)
        df = df.asfreq('D')

        return df
