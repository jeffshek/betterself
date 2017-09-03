import pandas as pd

from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, \
    VALID_PRODUCTIVITY_DRIVERS, SleepActivityDataframeBuilder, UserActivityEventDataframeBuilder
from analytics.events.utils.aggregate_dataframe_builders import AggregateSupplementProductivityDataframeBuilder
from apis.betterself.v1.correlations.serializers import CorrelationAnalyticsSerializer
from betterself.django_utils import days_ago_from_current_day
from constants import SLEEP_MINUTES_COLUMN
from events.models import SleepActivity, UserActivityEvent, SupplementEvent, DailyProductivityLog

NO_DATA_RESPONSE = Response([], content_type='application/json')


def get_sorted_response(series):
    if series.dropna().empty:
        return NO_DATA_RESPONSE

    # Do a odd sorted tuple response because Javascript sorting is an oddly difficult problem
    # sorted_response = [item for item in series.iteritems()]
    sorted_response = []
    for index, value in series.iteritems():
        if not pd.notnull(value):
            value = None

        data_point = (index, value)
        sorted_response.append(data_point)

    return Response(sorted_response)


class SleepUserActivitiesCorrelationView(APIView):
    def get(self, request):
        user = request.user

        sleep_activities = SleepActivity.objects.filter(user=user)
        sleep_serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate = sleep_serializer.get_sleep_history_series()

        if sleep_aggregate.empty:
            return NO_DATA_RESPONSE

        activity_events = UserActivityEvent.objects.filter(user=user)
        activity_serializer = UserActivityEventDataframeBuilder(activity_events)

        user_activity_dataframe = activity_serializer.get_flat_daily_dataframe()
        user_activity_dataframe[SLEEP_MINUTES_COLUMN] = sleep_aggregate

        correlation = user_activity_dataframe.corr()
        sleep_correlation = correlation[SLEEP_MINUTES_COLUMN].sort_values(ascending=False)
        return get_sorted_response(sleep_correlation)


class SleepSupplementsCorrelationView(APIView):
    def get(self, request):
        user = request.user
        queryset = SupplementEvent.objects.filter(user=user)
        supplements_df_builder = SupplementEventsDataframeBuilder(queryset)
        supplements_flat_daily_df = supplements_df_builder.get_flat_daily_dataframe()

        sleep_activities = SleepActivity.objects.filter(user=user)
        sleep_serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate_series = sleep_serializer.get_sleep_history_series()

        supplements_and_sleep_df = supplements_flat_daily_df.copy()
        supplements_and_sleep_df[SLEEP_MINUTES_COLUMN] = sleep_aggregate_series

        correlation = supplements_and_sleep_df.corr()
        sleep_correlation = correlation[SLEEP_MINUTES_COLUMN].sort_values(ascending=False)

        return get_sorted_response(sleep_correlation)


class ProductivitySupplementsCorrelationView(APIView):
    def get(self, request):
        user = request.user

        serializer = CorrelationAnalyticsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        correlation_lookback = serializer.validated_data['correlation_lookback']
        cumulative_lookback = serializer.validated_data['cumulative_lookback']

        # if we sum up cumulative days, need to look back even further to sum up the data
        days_to_look_back = correlation_lookback * cumulative_lookback
        cutoff_date = days_ago_from_current_day(days_to_look_back)

        correlation_driver = request.query_params.get('correlation_driver', 'Very Productive Minutes')
        if correlation_driver not in VALID_PRODUCTIVITY_DRIVERS:
            return Response('Invalid Correlation Driver Entered', status=400)

        aggregate_dataframe = AggregateSupplementProductivityDataframeBuilder.get_aggregate_dataframe_for_user(user,
            cutoff_date)
        if aggregate_dataframe.empty:
            return NO_DATA_RESPONSE

        if cumulative_lookback > 1:
            # min_periods of 1 allows for periods with no data to still be summed
            aggregate_dataframe = aggregate_dataframe.rolling(cumulative_lookback, min_periods=1).sum()

            # only include up to how many days the correlation lookback, otherwise incorrect overlap of correlations
            aggregate_dataframe = aggregate_dataframe[-correlation_lookback:]

        df_correlation = aggregate_dataframe.corr()
        df_correlation_driver_series = df_correlation[correlation_driver]

        # since this is a supplement only view, disregard how the other productivity drivers
        # ie. distracting minutes, neutral minutes might correlate with whatever is the productivity driver
        valid_index = [item for item in df_correlation_driver_series.index if item not in VALID_PRODUCTIVITY_DRIVERS]

        # but still include the correlation driver to make sure that the correlation of a variable with itself is 1
        valid_index.append(correlation_driver)

        filtered_correlation_series = df_correlation_driver_series[valid_index]
        filtered_correlation_series = filtered_correlation_series.sort_values(ascending=False)

        return get_sorted_response(filtered_correlation_series)


class ProductivityUserActivitiesCorrelationView(APIView):
    def get(self, request):
        user = request.user

        # TODO
        # 1) Switch to using an AggregateDataframe Builder instead of doing it by hand
        # 2) Include a hard-coded lookback of 60 days
        correlation_driver = request.query_params.get('correlation_driver', 'Very Productive Minutes')
        if correlation_driver not in VALID_PRODUCTIVITY_DRIVERS:
            return Response('Invalid Correlation Driver Entered', status=400)

        productivity_log = DailyProductivityLog.objects.filter(user=user)
        productivity_log_dataframe = AggregateSupplementProductivityDataframeBuilder.get_productivity_log_dataframe(
            productivity_log)
        if productivity_log_dataframe.empty:
            return NO_DATA_RESPONSE

        productivity_series = productivity_log_dataframe[correlation_driver]

        activity_events = UserActivityEvent.objects.filter(user=user)
        activity_serializer = UserActivityEventDataframeBuilder(activity_events)
        user_activity_dataframe = activity_serializer.get_flat_daily_dataframe()
        if user_activity_dataframe.empty:
            return NO_DATA_RESPONSE

        user_activity_dataframe[correlation_driver] = productivity_series

        correlation_dataframe = user_activity_dataframe.corr()
        correlation_driver_series = correlation_dataframe[correlation_driver]
        correlation_driver_series = correlation_driver_series.sort_values(ascending=False)

        return get_sorted_response(correlation_driver_series)
