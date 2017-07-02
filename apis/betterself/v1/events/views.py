import json

import numpy as np
import pandas as pd
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.betterself.v1.events.filters import SupplementEventFilter, UserActivityFilter, UserActivityEventFilter, \
    SleepActivityFilter
from apis.betterself.v1.events.serializers import SupplementEventCreateSerializer, SupplementEventReadOnlySerializer, \
    ProductivityLogReadSerializer, ProductivityLogCreateSerializer, UserActivitySerializer, \
    UserActivityEventCreateSerializer, UserActivityEventReadSerializer, UserActivityUpdateSerializer, \
    SleepActivityReadSerializer, SleepActivityCreateSerializer
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin
from config.pagination import ModifiedPageNumberPagination
from events.models import SupplementEvent, DailyProductivityLog, UserActivity, UserActivityEvent, SleepActivity


class SupplementEventView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin):
    model = SupplementEvent
    read_serializer_class = SupplementEventReadOnlySerializer
    write_serializer_class = SupplementEventCreateSerializer
    filter_class = SupplementEventFilter
    pagination_class = ModifiedPageNumberPagination

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related('supplement')

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()


class ProductivityLogView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin):
    model = DailyProductivityLog
    pagination_class = ModifiedPageNumberPagination
    read_serializer_class = ProductivityLogReadSerializer
    write_serializer_class = ProductivityLogCreateSerializer
    filter_fields = (
        'very_productive_time_minutes',
        'productive_time_minutes',
        'neutral_time_minutes',
        'distracting_time_minutes',
        'very_distracting_time_minutes',
        'uuid',
        'date',
    )

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserActivityView(ListCreateAPIView, UUIDDeleteMixin, UUIDUpdateMixin):
    model = UserActivity
    serializer_class = UserActivitySerializer
    filter_class = UserActivityFilter
    pagination_class = ModifiedPageNumberPagination
    update_serializer_class = UserActivityUpdateSerializer

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserActivityEventView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin):
    model = UserActivityEvent
    pagination_class = ModifiedPageNumberPagination
    read_serializer_class = UserActivityEventReadSerializer
    write_serializer_class = UserActivityEventCreateSerializer
    update_serializer_class = UserActivityEventCreateSerializer
    filter_class = UserActivityEventFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related('user_activity')


class SleepActivityView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin):
    model = SleepActivity
    pagination_class = ModifiedPageNumberPagination
    read_serializer_class = SleepActivityReadSerializer
    write_serializer_class = SleepActivityCreateSerializer
    filter_class = SleepActivityFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def round_timestamp_to_sleep_date(timeseries):
    """
    Not my proudest function ... this isn't as efficient as it could be, but struggling
    with some pandas syntax to find the perfect pandas one-line

    This can be much more performant, but need time to sit down and figure it out
    """
    sleep_dates = []
    for value in timeseries:
        if value.hour < 5:
            result = value - pd.DateOffset(days=1)
        else:
            result = value

        sleep_dates.append(result)

    index = pd.DatetimeIndex(sleep_dates)
    return index


class SleepAggregatesView(APIView):
    def get(self, request):
        user = request.user
        sleep_activities = SleepActivity.objects.filter(user=user)
        sleep_activities_values = sleep_activities.values('start_time', 'end_time')

        # for each given 24 hour period (ending at 2PM - the latest I can imagine someone might sleep in)
        # lot of mental debate here between calculating the sleep one gets from monday 10PM to tuesday 6AM as
        # either a Monday or Tuesday night, but I've decided to lean toward calculating that as Monday night
        dataframe = pd.DataFrame.from_records(sleep_activities_values)
        dataframe['sleep_time'] = dataframe['end_time'] - dataframe['start_time']

        sleep_index = round_timestamp_to_sleep_date(dataframe['end_time'])
        sleep_series = pd.Series(dataframe['sleep_time'].values, index=sleep_index)

        # get the sum of time slept during days (so this includes naps)
        # the result is timedeltas though, so convert below
        sleep_aggregate = sleep_series.resample('D').sum()

        # change from timedeltas to minutes, otherwise json response of timedelta is garbage
        sleep_aggregate = sleep_aggregate / np.timedelta64(1, 'm')

        # this is crap, there's got to be something you're doing wrong with pandas json...
        # otherwise, the result is coming as one crappy string
        # so this is a hack to spit it to json and pass the data to the frontend
        result = sleep_aggregate.to_json(date_format='iso')
        result = json.loads(result)

        return Response(data=result, status=200, content_type='application/json')


class SleepAveragesView(APIView):
    def get(self, request):
        return Response(status=200)


class SleepActivitiesCorrelationView(APIView):
    def get(self, request):
        return Response(status=200)


class SleepSupplementsCorrelationView(APIView):
    def get(self, request):
        return Response(status=200)
