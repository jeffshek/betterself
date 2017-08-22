from rest_framework import serializers

from events.models import SleepActivity


class FitbitAPIRequestSerializer(serializers.Serializer):
    # add a check to make sure end_date is greater than start_date
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('Finish must occur after start')

        # Do something to be nice to vendor's servers
        days_difference = data['end_date'] - data['start_date']
        if days_difference.days > 370:
            raise serializers.ValidationError('Start and end dates must be within 370 days')

        return data


class FitbitResponseSleepActivitySerializer(serializers.ModelSerializer):
    source = serializers.CharField(default='api')

    class Meta:
        model = SleepActivity
        fields = ('start_time', 'end_time', 'source', 'user')

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError('Finish must occur after start')

        return data

    def create(self, data):
        user = data['user']
        # serializers automatically assume everything is utc, but that's a lie, so take
        # out the UTC info
        start_time = data['start_time'].replace(tzinfo=None)
        end_time = data['end_time'].replace(tzinfo=None)

        # fitbit doesn't give timezone aware objects, so convert it here prior to saving
        # NOTE: Don't use replace to swap out UTC to another timezone, it has very odd
        # consequences! In short, just assume it's buggy and try to use it almost never!
        start_time_local = user.pytz_timezone.localize(start_time)
        end_time_local = user.pytz_timezone.localize(end_time)

        # if we find any overlapping periods, delete them
        overlaps = SleepActivity.objects.filter(user=user, end_time__gte=start_time_local,
                                                start_time__lte=end_time_local)
        overlaps.delete()

        instance = SleepActivity.objects.create(user=user, end_time=end_time_local, start_time=start_time_local,
                                                source=data['source'])
        return instance
