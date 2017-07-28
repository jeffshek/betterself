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
        return data
