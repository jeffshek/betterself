import factory
from django.utils import timezone

from events.models import SupplementEvent, DailyProductivityLog
from supplements.fixtures.factories import SupplementFactory


class SupplementEventFactory(factory.DjangoModelFactory):
    source = 'api'
    supplement = factory.SubFactory(SupplementFactory)
    quantity = 1
    time = timezone.now()

    class Meta:
        model = SupplementEvent


class DailyProductivityLogFactory(factory.DjangoModelFactory):
    source = 'api'

    very_productive_time_minutes = 10
    productive_time_minutes = 20
    neutral_time_minutes = 30
    distracting_time_minutes = 40
    very_distracting_time_minutes = 50

    class Meta:
        model = DailyProductivityLog
