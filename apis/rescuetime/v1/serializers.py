from rest_framework import serializers


class UpdateRescueTimeAPISerializer(serializers.Serializer):
    rescuetime_api_key = serializers.CharField(max_length=200)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
