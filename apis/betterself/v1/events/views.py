import json

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.betterself.v1.events.filters import SupplementEventFilter, UserActivityFilter, UserActivityEventFilter, \
    SleepActivityFilter
from apis.betterself.v1.events.serializers import SupplementEventCreateSerializer, SupplementEventReadOnlySerializer, \
    ProductivityLogReadSerializer, ProductivityLogCreateSerializer, UserActivitySerializer, \
    UserActivityEventCreateSerializer, UserActivityEventReadSerializer, UserActivityUpdateSerializer, \
    SleepActivityReadSerializer, SleepActivityCreateSerializer, SleepActivityDataframeBuilder, \
    UserActivityEventDataframeBuilder
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin
from config.pagination import ModifiedPageNumberPagination
from constants import SLEEP_MINUTES_COLUMN, LOOKBACK_PARAM_NAME
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


class SleepAggregatesView(APIView):
    def get(self, request):
        user = request.user
        sleep_activities = SleepActivity.objects.filter(user=user)

        serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate = serializer.get_sleep_history()

        # because pandas uses a timeindex, when we go to json - it doesn't
        # play nicely with a typical json dump, so we do an additional load so drf can transmit nicely
        result = sleep_aggregate.to_json(date_format='iso')
        result = json.loads(result)
        return Response(data=result, content_type='application/json')


class SleepAveragesView(APIView):
    def get(self, request):
        try:
            lookback = int(request.query_params[LOOKBACK_PARAM_NAME])
        except (ValueError, MultiValueDictKeyError):
            # MultiValueDictKeyError when a key doesn't exist
            # ValueError if something entered for a lookback that couldn't be interpreted
            return Response(status=400)

        user = request.user
        sleep_activities = SleepActivity.objects.filter(user=user)

        serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate = serializer.get_sleep_history()

        sleep_average = sleep_aggregate.rolling(window=lookback).mean()

        result = sleep_average.to_json(date_format='iso')
        result = json.loads(result)
        return Response(data=result, content_type='application/json')


class SleepActivitiesCorrelationView(APIView):
    def get(self, request):
        user = request.user

        sleep_activities = SleepActivity.objects.filter(user=user)
        sleep_serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate = sleep_serializer.get_sleep_history()

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
        return Response(status=200)
