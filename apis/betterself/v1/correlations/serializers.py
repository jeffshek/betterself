from rest_framework import serializers

from analytics.events.utils.dataframe_builders import PRODUCTIVITY_DRIVERS_KEYS, VERY_PRODUCTIVE_TIME_LABEL


class CorrelationsAndRollingLookbackRequestSerializer(serializers.Serializer):
    correlation_lookback = serializers.IntegerField(default=60, min_value=1, max_value=365)
    cumulative_lookback = serializers.IntegerField(default=1, min_value=1, max_value=365)
    correlation_driver = serializers.ChoiceField(choices=PRODUCTIVITY_DRIVERS_KEYS,
                                                 default=VERY_PRODUCTIVE_TIME_LABEL)
