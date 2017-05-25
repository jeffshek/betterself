from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from apis.betterself.v1.events.filters import SupplementEventFilter
from apis.betterself.v1.events.serializers import SupplementEventCreateSerializer, SupplementEventReadOnlySerializer, \
    ProductivityLogReadSerializer, ProductivityLogCreateSerializer
from apis.betterself.v1.utils.views import BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1
from config.pagination import ModifiedPageNumberPagination
from events.models import SupplementEvent, DailyProductivityLog


class SupplementEventView(BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1, RetrieveUpdateDestroyAPIView):
    model = SupplementEvent
    read_serializer_class = SupplementEventReadOnlySerializer
    write_serializer_class = SupplementEventCreateSerializer
    filter_class = SupplementEventFilter
    pagination_class = ModifiedPageNumberPagination

    def get_queryset(self):
        return super().get_queryset().select_related('supplement')

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def destroy(self, request, *args, **kwargs):
        try:
            uuid = request.data['uuid']
        except KeyError:
            raise Http404

        filter_params = {
            'uuid': uuid,
            'user': request.user
        }

        object = get_object_or_404(self.model, **filter_params)
        object.delete()
        return Response(status=204)


class ProductivityLogView(BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1):
    model = DailyProductivityLog
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
