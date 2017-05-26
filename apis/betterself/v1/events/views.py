from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from apis.betterself.v1.events.filters import SupplementEventFilter
from apis.betterself.v1.events.serializers import SupplementEventCreateSerializer, SupplementEventReadOnlySerializer, \
    ProductivityLogReadSerializer, ProductivityLogCreateSerializer
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin
from config.pagination import ModifiedPageNumberPagination
from events.models import SupplementEvent, DailyProductivityLog


class SupplementEventView(GenericAPIView, ListModelMixin, CreateModelMixin, ReadOrWriteSerializerChooser,
                          UUIDDeleteMixin):
    model = SupplementEvent
    read_serializer_class = SupplementEventReadOnlySerializer
    write_serializer_class = SupplementEventCreateSerializer
    filter_class = SupplementEventFilter
    pagination_class = ModifiedPageNumberPagination

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related('supplement')

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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
