from rest_framework import serializers

from constants import SLEEP_MINUTES_COLUMN, VERY_PRODUCTIVE_TIME_LABEL, PRODUCTIVITY_DRIVERS_KEYS


class ProductivityRequestParamsSerializer(serializers.Serializer):
    correlation_lookback = serializers.IntegerField(default=60, min_value=1, max_value=365)
    cumulative_lookback = serializers.IntegerField(default=1, min_value=1, max_value=365)
    correlation_driver = serializers.ChoiceField(choices=PRODUCTIVITY_DRIVERS_KEYS,
                                                 default=VERY_PRODUCTIVE_TIME_LABEL)


class SleepRequestParamsSerializer(serializers.Serializer):
    correlation_lookback = serializers.IntegerField(default=60, min_value=1, max_value=365)
    cumulative_lookback = serializers.IntegerField(default=1, min_value=1, max_value=365)
    # Kind of odd, but the only correlation_driver should be SLEEP_MINUTES_COLUMN unlike productivity
    # in the future this might change because FitBit has tiered levels of sleep, but you ain't there yet
    correlation_driver = serializers.ChoiceField(choices=[SLEEP_MINUTES_COLUMN], default=SLEEP_MINUTES_COLUMN)


# TODO
# desired names are
# rollingWindow
# lookbackHistory
