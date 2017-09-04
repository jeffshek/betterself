from rest_framework import serializers


class CorrelationsAndRollingLookbackRequestSerializer(serializers.Serializer):
    correlation_lookback = serializers.IntegerField(default=60, min_value=1, max_value=365)
    cumulative_lookback = serializers.IntegerField(default=1, min_value=1, max_value=365)
