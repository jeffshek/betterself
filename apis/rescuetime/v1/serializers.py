from rest_framework import serializers


class RescueTimeAPIRequestSerializer(serializers.Serializer):
    rescuetime_api_key = serializers.CharField(max_length=200)
    # add a check to make sure end_date is greater than start_date
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('Finish must occur after start')

        # Do something to be nice to RescueTime's servers
        days_difference = data['end_date'] - data['start_date']
        if days_difference.days > 370:
            raise serializers.ValidationError('Start and end dates must be within 370 days')

        return data
