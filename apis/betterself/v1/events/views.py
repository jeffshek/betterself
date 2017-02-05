from apis.betterself.v1.events.filters import SupplementEventFilter
from apis.betterself.v1.events.serializers import SupplementEventCreateSerializer, SupplementEventReadOnlySerializer, \
    ProductivityLogReadSerializer, ProductivityLogCreateSerializer
from apis.betterself.v1.utils.views import BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1
from events.models import SupplementEvent, DailyProductivityLog


class SupplementEventView(BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1):
    model = SupplementEvent
    read_serializer_class = SupplementEventReadOnlySerializer
    write_serializer_class = SupplementEventCreateSerializer
    filter_class = SupplementEventFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()


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
