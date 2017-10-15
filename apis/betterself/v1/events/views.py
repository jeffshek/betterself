import datetime
import json
import pandas as pd
from dateutil import relativedelta

from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.events.utils.dataframe_builders import ProductivityLogEventsDataframeBuilder, \
    SupplementEventsDataframeBuilder, SleepActivityDataframeBuilder
from apis.betterself.v1.constants import DAILY_FREQUENCY, MONTHLY_FREQUENCY
from apis.betterself.v1.events.filters import SupplementEventFilter, UserActivityFilter, UserActivityEventFilter, \
    DailyProductivityLogFilter
from apis.betterself.v1.events.serializers import SupplementEventCreateUpdateSerializer, \
    SupplementEventReadOnlySerializer, ProductivityLogReadSerializer, ProductivityLogCreateSerializer, \
    UserActivitySerializer, UserActivityEventCreateSerializer, UserActivityEventReadSerializer, \
    UserActivityUpdateSerializer, ProductivityLogRequestParametersSerializer, \
    SupplementLogRequestParametersSerializer, SupplementReminderReadSerializer, SupplementReminderCreateSerializer
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin
from betterself.utils.date_utils import get_current_userdate
from betterself.utils.pandas_utils import force_start_end_date_to_series, force_start_end_data_to_dataframe, \
    update_dataframe_to_be_none_instead_of_nan_for_api_responses
from config.pagination import ModifiedPageNumberPagination
from events.models import SupplementLog, DailyProductivityLog, UserActivity, UserActivityLog, SupplementReminder, \
    SleepLog
from supplements.models import Supplement


class SupplementEventView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin):
    model = SupplementLog
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
    # TODO - Refactor all of this after Twilio integration!
    def get(self, request):
        user = request.user

        serializer = ProductivityLogRequestParametersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_params = serializer.validated_data
        query_start_date = query_params['start_date']
        query_cumulative_window = query_params['cumulative_window']
        complete_date_range_in_daily_frequency = query_params['complete_date_range_in_daily_frequency']

        # if this is a cumulative window, we want to look back even further when filtering
        log_filter_date = query_start_date - relativedelta.relativedelta(days=query_cumulative_window)

        productivity_logs = DailyProductivityLog.objects.filter(user=user, date__gte=log_filter_date)

        # data is consumed by front-end, so don't rename columns
        dataframe_builder = ProductivityLogEventsDataframeBuilder(productivity_logs, rename_columns=False)
        results = dataframe_builder.get_flat_daily_dataframe()

        # TODO - feels like we should always just do this from the builder level to be on the safe side ...
        results.sort_index(ascending=True, inplace=True)

        # sum up the history by how many days as the window specifies
        results = results.rolling(window=query_cumulative_window, min_periods=1).sum()

        # because rolling windows need to look back further to sum, this timeseries has extra dates
        results = results[query_start_date:]

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
    model = UserActivityLog
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
    # TODO - Refactor all of this after Twilio integration!
    def get(self, request, supplement_uuid):
        supplement = get_object_or_404(Supplement, uuid=supplement_uuid, user=request.user)
        user = request.user

        serializer = SupplementLogRequestParametersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        start_date = params['start_date']
        end_date = get_current_userdate(user)

        supplement_events = SupplementLog.objects.filter(user=user, supplement=supplement, time__date__gte=start_date)

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


class SupplementReminderView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin):
    model = SupplementReminder
    write_serializer_class = SupplementReminderCreateSerializer
    read_serializer_class = SupplementReminderReadSerializer

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related('supplement')

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()


class AggregatedSupplementLogView(APIView):
    # TODO - Refactor all of this after Twilio integration! Wow, this view sucks
    """ Returns a list of dates that Supplement was taken along with the productivity and sleep of that date"""

    def get(self, request, supplement_uuid):
        # TODO - Refactor this garbage, you can add some smart redis caching level to this

        supplement = get_object_or_404(Supplement, uuid=supplement_uuid, user=request.user)
        user = request.user

        serializer = SupplementLogRequestParametersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        start_date = params['start_date']
        end_date = get_current_userdate(user)

        supplement_events = SupplementLog.objects.filter(
            user=user, supplement=supplement, time__date__gte=start_date, time__date__lte=end_date)

        # no point if nothing exists
        if not supplement_events.exists():
            return Response([])

        # lots of crappy templating here, sorry.
        supplement_builder = SupplementEventsDataframeBuilder(supplement_events)
        # TODO - Really feels like you should build a helper on the builder to do this since you do it so often
        supplement_series = supplement_builder.build_dataframe()['Quantity'].sort_index()

        # because the dataframe will also get things like "source" etc, and we only care about
        # quantity, take that series and then recast it as a numeric
        supplement_series = pd.to_numeric(supplement_series)

        productivity_logs = DailyProductivityLog.objects.filter(
            user=user, date__gte=start_date, date__lte=end_date)
        productivity_builder = ProductivityLogEventsDataframeBuilder(productivity_logs)
        productivity_series = productivity_builder.get_productive_timeseries()

        sleep_logs = SleepLog.objects.filter(user=user, start_time__date__gte=start_date)
        sleep_builder = SleepActivityDataframeBuilder(sleep_logs, user)
        sleep_series = sleep_builder.get_sleep_history_series()

        dataframe_details = {
            'sleep_time': sleep_series,
            'productivity_time': productivity_series,
            'quantity': supplement_series,
        }

        dataframe = pd.DataFrame(dataframe_details)
        # don't really need to convert it to local, just makes debugging make easier
        dataframe_localized = dataframe.tz_convert(user.pytz_timezone)

        """
        because events are datetime based, but productivity and sleep are date-based
        this parts get a little hairy, but we want the nans for 8/30 and 9/01 to be filled
        however, we cant just pad fill because if a log for productivity and sleep was missing
        the wrong result would be filled. so ... the code below is slightly magical


                                    productivity_time       sleep_time  quantity
        2017-08-30 00:00:00-04:00               1336.0  647.013778         0.0
        2017-08-30 19:51:36.483443-04:00           NaN         NaN         1.0
        2017-08-31 00:00:00-04:00               1476.0  726.132314         0.0
        2017-09-01 00:00:00-04:00                730.0  513.894938         0.0
        2017-09-01 14:51:36.483443-04:00           NaN         NaN         1.0
        """
        if not params['frequency']:
            dataframe_localized_date_index = dataframe_localized.index.date
            dataframe_localized_date_index = pd.DatetimeIndex(dataframe_localized_date_index,
                tz=request.user.pytz_timezone)

            productivity_series = dataframe_localized['productivity_time'].dropna()
            productivity_series_filled = productivity_series[dataframe_localized_date_index]

            sleep_series = dataframe_localized['sleep_time'].dropna()
            sleep_series_filled = sleep_series[dataframe_localized_date_index]

            dataframe_localized['productivity_time'] = productivity_series_filled.values
            dataframe_localized['sleep_time'] = sleep_series_filled.values

            valid_supplement_index = dataframe_localized['quantity'].dropna().index
            dataframe_localized = dataframe_localized.ix[valid_supplement_index]

        elif params['frequency'] == DAILY_FREQUENCY:
            dataframe_localized = dataframe_localized.resample('D').sum()

        elif params['frequency'] == MONTHLY_FREQUENCY:
            dataframe_localized = dataframe_localized.resample('M').sum()

        dataframe_localized = update_dataframe_to_be_none_instead_of_nan_for_api_responses(dataframe_localized)

        results = []
        for index, values in dataframe_localized.iterrows():
            time = index.isoformat()
            result = values.to_dict()
            result['time'] = time
            result['uniqueKey'] = '{}-{}'.format(time, result['quantity'])

            results.append(result)

        return Response(results)
