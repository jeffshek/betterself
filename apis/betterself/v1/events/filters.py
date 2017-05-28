import django_filters
from django_filters.rest_framework import FilterSet

from events.models import SupplementEvent, UserActivity, UserActivityEvent


class SupplementEventFilter(FilterSet):
    supplement_uuid = django_filters.UUIDFilter(name='supplement__uuid')

    class Meta:
        model = SupplementEvent
        fields = [
            'supplement_uuid',
            'quantity',
            'time',
            'source',
            'uuid',
        ]


class UserActivityFilter(FilterSet):
    class Meta:
        model = UserActivity
        fields = [
            'name',
            'uuid',
        ]


class UserActivityEventFilter(FilterSet):
    class Meta:
        model = UserActivityEvent
        fields = [
            'uuid',
            'duration_minutes'
        ]
