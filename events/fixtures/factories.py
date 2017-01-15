import factory
from django.utils import timezone

from events.models import SupplementEvent
from supplements.fixtures.factories import SupplementFactory


class SupplementEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = SupplementEvent

    source = 'api'
    supplement = factory.SubFactory(SupplementFactory)
    quantity = 1
    time = timezone.now()
