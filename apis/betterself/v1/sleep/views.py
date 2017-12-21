import json

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.betterself.v1.events.filters import SleepLogFilter
from apis.betterself.v1.events.serializers import SleepLogReadSerializer, SleepLogCreateSerializer
from analytics.events.utils.dataframe_builders import SleepActivityDataframeBuilder
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin
from config.pagination import ModifiedPageNumberPagination
from constants import LOOKBACK_PARAM_NAME
from events.models import SleepLog


class SleepActivityView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin):
    model = SleepLog
    pagination_class = ModifiedPageNumberPagination
    read_serializer_class = SleepLogReadSerializer
    write_serializer_class = SleepLogCreateSerializer
    filter_class = SleepLogFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class SleepAggregatesView(APIView):
    def get(self, request):
        user = request.user
        sleep_activities = SleepLog.objects.filter(user=user)

        serializer = SleepActivityDataframeBuilder(sleep_activities)
        sleep_aggregate = serializer.get_sleep_history_series()

        # because pandas uses a timeindex, when we go to json - it doesn't
        # play nicely with a typical json dump, so we do an additional load so drf can transmit nicely
        result = sleep_aggregate.to_json(date_format='iso')
        result = json.loads(result)
        return Response(data=result)


class SleepAveragesView(APIView):
    def get(self, request):
        try:
            window = int(request.query_params[LOOKBACK_PARAM_NAME])
        except MultiValueDictKeyError:
            # MultiValueDictKeyError happens when a key doesn't exist
            window = 1
        except ValueError:
            # ValueError if something entered for a window that couldn't be interpreted
            return Response(status=400)

        user = request.user

        sleep_activities = SleepLog.objects.filter(user=user)
        builder = SleepActivityDataframeBuilder(sleep_activities)

        sleep_aggregate = builder.get_sleep_history_series()
        sleep_average = sleep_aggregate.rolling(window=window, min_periods=1).mean()

        result = sleep_average.to_json(date_format='iso')
        result = json.loads(result)
        return Response(data=result)
