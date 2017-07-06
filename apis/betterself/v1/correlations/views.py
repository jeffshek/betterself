from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder
from apis.betterself.v1.events.serializers import SleepActivityDataframeBuilder, UserActivityEventDataframeBuilder
from constants import SLEEP_MINUTES_COLUMN
from events.models import SleepActivity, UserActivityEvent, SupplementEvent


class SleepActivitiesCorrelationView(APIView):
    def get(self, request):
        user = request.user

        sleep_activities = SleepActivity.objects.filter(user=user)
        sleep_serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate = sleep_serializer.get_sleep_history()

        if sleep_aggregate.empty:
            return Response({})

        # resample so that it goes from no frequency to a daily frequency
        # which matches UserActivityEvents, eventually need to be more elegant
        sleep_aggregate = sleep_aggregate.resample('D').last()

        activity_events = UserActivityEvent.objects.filter(user=user)
        activity_serializer = UserActivityEventDataframeBuilder(activity_events)

        user_activity_dataframe = activity_serializer.get_user_activity_events()
        user_activity_dataframe[SLEEP_MINUTES_COLUMN] = sleep_aggregate

        correlation = user_activity_dataframe.corr()
        sleep_correlation = correlation[SLEEP_MINUTES_COLUMN].sort_values()
        return Response(sleep_correlation.to_dict())


class SleepSupplementsCorrelationView(APIView):
    def get(self, request):
        user = request.user
        queryset = SupplementEvent.objects.filter(user=user)
        supplements_df_builder = SupplementEventsDataframeBuilder(queryset)
        supplements_flat_daily_df = supplements_df_builder.get_flat_daily_dataframe()

        sleep_activities = SleepActivity.objects.filter(user=user)
        sleep_serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate_series = sleep_serializer.get_sleep_history()
        try:
            # attempt to normalize to hold sleep_aggregate_series only dates
            sleep_aggregate_series.index = sleep_aggregate_series.index.date
        except AttributeError:
            pass

        supplements_and_sleep_df = supplements_flat_daily_df.copy()
        supplements_and_sleep_df[SLEEP_MINUTES_COLUMN] = sleep_aggregate_series

        correlation = supplements_and_sleep_df.corr()
        sleep_correlation = correlation[SLEEP_MINUTES_COLUMN].sort_values(ascending=False)

        # Do a odd sorted tuple response because Javascript sorting is an oddly difficult problem
        sorted_response = [item for item in sleep_correlation.iteritems()]
        return Response(sorted_response)
