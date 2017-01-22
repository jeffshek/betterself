import django_filters
from django_filters.rest_framework import FilterSet

from events.models import SupplementEvent


class SupplementEventFilter(FilterSet):
    supplement_uuid = django_filters.UUIDFilter(name='supplement__uuid')
    quantity = django_filters.NumberFilter(name='quantity')
    time = django_filters.DateTimeFilter(name='time')
    source = django_filters.CharFilter(name='source')

    class Meta:
        model = SupplementEvent
        fields = [
            'supplement_uuid',
            'quantity',
            'time',
            'source',
            'uuid',
        ]
