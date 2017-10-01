import datetime
import json
import pandas as pd

from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.events.utils.dataframe_builders import ProductivityLogEventsDataframeBuilder, \
    SupplementEventsDataframeBuilder
from apis.betterself.v1.events.filters import SupplementEventFilter, UserActivityFilter, UserActivityEventFilter, \
    DailyProductivityLogFilter
from apis.betterself.v1.events.serializers import SupplementEventCreateUpdateSerializer, \
    SupplementEventReadOnlySerializer, ProductivityLogReadSerializer, ProductivityLogCreateSerializer, \
    UserActivitySerializer, UserActivityEventCreateSerializer, UserActivityEventReadSerializer, \
    UserActivityUpdateSerializer, ProductivityLogRequestParametersSerializer, \
    SupplementLogRequestParametersSerializer, SupplementReminderSerializer
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin
from betterself.utils.pandas_utils import force_start_end_date_to_series, force_start_end_data_to_dataframe
from config.pagination import ModifiedPageNumberPagination
from events.models import SupplementEvent, DailyProductivityLog, UserActivity, UserActivityEvent, SupplementReminder
from supplements.models import Supplement


class SupplementEventView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin):
    model = SupplementEvent
    read_serializer_class = SupplementEventReadOnlySerializer
    write_serializer_class = SupplementEventCreateUpdateSerializer
    update_serializer_class = SupplementEventCreateUpdateSerializer
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
    filter_class = DailyProductivityLogFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ProductivityLogAggregatesView(APIView):
    def get(self, request):
        user = request.user

        serializer = ProductivityLogRequestParametersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_params = serializer.validated_data
        query_start_date = query_params['start_date']
        query_cumulative_window = query_params['cumulative_window']
        complete_date_range_in_daily_frequency = query_params['complete_date_range_in_daily_frequency']

        productivity_logs = DailyProductivityLog.objects.filter(user=user, date__gte=query_start_date)

        # data is consumed by front-end, so don't rename columns
        dataframe_builder = ProductivityLogEventsDataframeBuilder(productivity_logs, rename_columns=False)
        results = dataframe_builder.get_flat_daily_dataframe()

        # TODO - feels like we should always just do this from the builder level to be on the safe side ...
        results.sort_index(ascending=True, inplace=True)

        # sum up the history by how many days as the window specifies
        results = results.rolling(window=query_cumulative_window, min_periods=1).sum()

        if complete_date_range_in_daily_frequency:
            results = force_start_end_data_to_dataframe(user, results, query_start_date, datetime.date.today())

        data_formatted = json.loads(results.to_json(date_format='iso', orient='index', double_precision=2))
        return Response(data_formatted)


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


class SupplementLogListView(APIView):
    def get(self, request, supplement_uuid):
        supplement = get_object_or_404(Supplement, uuid=supplement_uuid, user=request.user)
        user = request.user

        serializer = SupplementLogRequestParametersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        start_date = params['start_date']
        end_date = datetime.datetime.now(user.pytz_timezone).date()

        supplement_events = SupplementEvent.objects.filter(user=user, supplement=supplement, time__date__gte=start_date)

        builder = SupplementEventsDataframeBuilder(supplement_events)
        if params['frequency'] == 'daily':
            # most of the time the dataframe contains a lot of supplements, here we are only picking one
            try:
                series = builder.get_flat_daily_dataframe()[supplement.name]
            except KeyError:
                # key error for no data if the supplement was never taken during this time
                series = pd.Series()

            if params['complete_date_range_in_daily_frequency']:
                series = force_start_end_date_to_series(user, series, start_date, end_date)

        else:
            df = builder.build_dataframe()
            series = df['Quantity']

        json_data = series.to_json(date_format='iso')
        data = json.loads(json_data)
        return Response(data)


class SupplementReminderView(ListCreateAPIView, UUIDDeleteMixin, UUIDUpdateMixin):
    model = SupplementReminder
    serializer_class = SupplementReminderSerializer

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related('supplement', 'user')
