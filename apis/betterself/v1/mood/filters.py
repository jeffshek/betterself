from django_filters.rest_framework import FilterSet

from events.models import UserMoodLog


class UserMoodLogFilter(FilterSet):
    class Meta:
        model = UserMoodLog
        fields = [
            'uuid',
            'value',
            'time',
        ]
