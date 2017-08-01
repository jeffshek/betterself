import django_filters
from django_filters.rest_framework import FilterSet

from events.models import SupplementEvent, UserActivity, UserActivityEvent, SleepActivity, DailyProductivityLog


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
    user_activity_uuid = django_filters.UUIDFilter(name='user_activity__uuid')

    class Meta:
        model = UserActivityEvent
        fields = [
            'uuid',
            'time',
            'duration_minutes',
            'user_activity_uuid'
        ]


class SleepActivityFilter(FilterSet):
    class Meta:
        model = SleepActivity
        fields = [
            'uuid',
            'start_time',
            'end_time',
        ]


class DailyProductivityLogFilter(FilterSet):
    start_date = django_filters.DateFilter(name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(name='date', lookup_expr='lte')

    class Meta:
        model = DailyProductivityLog
        fields = [
            'uuid',
            'date',
            'source',
            'very_productive_time_minutes',
            'productive_time_minutes',
            'neutral_time_minutes',
            'distracting_time_minutes',
            'very_distracting_time_minutes',
            'start_date',
            'end_date'
        ]
