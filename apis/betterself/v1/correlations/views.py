import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.events.utils.aggregate_dataframe_builders import AggregateSupplementProductivityDataframeBuilder, \
    AggregateUserActivitiesEventsProductivityActivitiesBuilder, AggregateSleepActivitiesUserActivitiesBuilder, \
    AggregateSleepActivitiesSupplementsBuilder
from analytics.events.utils.dataframe_builders import PRODUCTIVITY_DRIVERS_LABELS
from apis.betterself.v1.correlations.serializers import ProductivityRequestParamsSerializer, \
    SleepRequestParamsSerializer
from betterself.utils.date_utils import days_ago_from_current_day
from constants import SLEEP_MINUTES_COLUMN

NO_DATA_RESPONSE = Response([])


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


class CorrelationsAPIView(APIView):
    """ Centralizes all the logic for getting dataframe and correlating them to Productivity """

    def get(self, request):
        user = request.user

        serializer = self.request_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        correlation_lookback = serializer.validated_data['correlation_lookback']
        cumulative_lookback = serializer.validated_data['cumulative_lookback']
        correlation_driver = serializer.validated_data['correlation_driver']

        # if we sum up cumulative days, need to look back even further to sum up the data
        days_to_look_back = correlation_lookback * cumulative_lookback
        cutoff_date = days_ago_from_current_day(days_to_look_back)

        aggregate_dataframe = self.dataframe_builder.get_aggregate_dataframe_for_user(user, cutoff_date)
        if aggregate_dataframe.empty:
            return NO_DATA_RESPONSE

        if cumulative_lookback > 1:
            # min_periods of 1 allows for periods with no data to still be summed
            aggregate_dataframe = aggregate_dataframe.rolling(cumulative_lookback, min_periods=1).sum()

            # only include up to how many days the correlation lookback, otherwise incorrect overlap of correlations
            aggregate_dataframe = aggregate_dataframe[-correlation_lookback:]

        df_correlation = aggregate_dataframe.corr()
        df_correlation_series = df_correlation[correlation_driver]

        # disregard all other valid correlation drivers and only care about the variables
        # ie. distracting minutes, neutral minutes might correlate with whatever is the productivity driver
        valid_index = [item for item in df_correlation_series.index if item not in self.valid_correlations]

        # but still include the correlation driver to make sure that the correlation of a variable with itself is 1
        # seeing something correlate with itself of 1 is soothing to know its not flawed
        valid_index.append(correlation_driver)

        filtered_correlation_series = df_correlation_series[valid_index]
        filtered_correlation_series = filtered_correlation_series.sort_values(ascending=False)

        return get_sorted_response(filtered_correlation_series)


class ProductivityLogsSupplementsCorrelationsView(CorrelationsAPIView):
    dataframe_builder = AggregateSupplementProductivityDataframeBuilder
    valid_correlations = PRODUCTIVITY_DRIVERS_LABELS
    request_serializer = ProductivityRequestParamsSerializer


class ProductivityLogsUserActivitiesCorrelationsView(CorrelationsAPIView):
    dataframe_builder = AggregateUserActivitiesEventsProductivityActivitiesBuilder
    valid_correlations = PRODUCTIVITY_DRIVERS_LABELS
    request_serializer = ProductivityRequestParamsSerializer


class SleepActivitiesUserActivitiesCorrelationsView(CorrelationsAPIView):
    dataframe_builder = AggregateSleepActivitiesUserActivitiesBuilder
    valid_correlations = [SLEEP_MINUTES_COLUMN]
    request_serializer = SleepRequestParamsSerializer


class SleepActivitiesSupplementsCorrelationsView(CorrelationsAPIView):
    dataframe_builder = AggregateSleepActivitiesSupplementsBuilder
    valid_correlations = [SLEEP_MINUTES_COLUMN]
    request_serializer = SleepRequestParamsSerializer
