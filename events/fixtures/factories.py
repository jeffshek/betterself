import datetime
import factory

from events.models import SupplementEvent
from supplements.fixtures.factories import SupplementFactory


class SupplementEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = SupplementEvent

    source = 'api'
    supplement_product = factory.SubFactory(SupplementFactory)
    quantity = 1
    time = datetime.datetime.now()
