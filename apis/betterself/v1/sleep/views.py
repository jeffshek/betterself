import json

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.betterself.v1.events.filters import SleepActivityFilter
from apis.betterself.v1.events.serializers import SleepActivityReadSerializer, SleepActivityCreateSerializer, \
    SleepActivityDataframeBuilder
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin
from config.pagination import ModifiedPageNumberPagination
from constants import LOOKBACK_PARAM_NAME
from events.models import SleepActivity


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
